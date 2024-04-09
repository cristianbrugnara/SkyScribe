import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Reshape, Dense, Bidirectional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from .get_dataset import mongo_to_dataframe
from typing import List


class Forecaster:
    def __init__(self, station_id : int, input_fields : List[str] = None, output_fields : List[str] = None,
                 input_steps : int = 300, horizon_steps : int = 250):
        self.__stat_id = station_id
        self.__input_fields = input_fields
        self.__output_fields = output_fields
        self.__input_steps = input_steps
        self.__horizon_steps = horizon_steps

        self.__to_update = False
        self.update_data(self.input_fields, self.__output_fields)
        self.__to_update = True

        self.__X_train = None
        self.__y_train = None
        self.__X_test = None
        self.__model = None
        self.__optim=None
        self.__loss=None

    @property
    def input_fields(self):
        return self.__input_fields

    @property
    def output_fields(self):
        return self.__output_fields

    def preprocess(self):
        self.__ts_column = self.__df.pop('ts')
        input_normalizer = MinMaxScaler()
        self.__normalizer_used = MinMaxScaler()

        if self.output_fields:
            self.__df[self.output_fields] = self.__normalizer_used.fit_transform(self.__df[self.output_fields])
        else:
            self.__df[self.__df.columns] = self.__normalizer_used.fit_transform(self.__df[self.__df.columns])

        if self.input_fields:
            self.__df[self.input_fields] = input_normalizer.fit_transform(self.__df[self.input_fields])

        else:
            self.__df[self.__df.columns] = input_normalizer.fit_transform(self.__df[self.__df.columns])

    def update_data(self, input_fields = None, output_fields = None):
        if input_fields:
            self.__input_fields = input_fields
        else:
            self.__input_fields = None    # need this for update model method if going from having fields to all fields

        if output_fields:
            self.__output_fields = output_fields
        else:
            self.__output_fields = None

        if not input_fields or not output_fields:
            to_keep = 'all'
        else:
            to_keep = {el: 1 for el in set(self.__input_fields + self.__output_fields)}
            to_keep['ts']=1

        self.__df = mongo_to_dataframe(self.__stat_id, to_keep)
        self.preprocess()

        if self.__to_update:
            self.create_model(self.__optim, self.__loss)

    def make_window(self,X, y,input_steps : int, horizon_steps : int):
        X_res, y_res = [], []

        for i in range(len(X) - input_steps - horizon_steps + 1):
            X_res.append(X.iloc[i : i+input_steps].to_numpy())
            y_res.append(y.iloc[i+input_steps : i+input_steps+horizon_steps])

        return np.array(X_res), np.array(y_res)

    def split(self):
        X, y = self.__df, self.__df,
        if self.input_fields:
            X = self.__df[self.input_fields]
        if self.output_fields:
            y = self.__df[self.output_fields]

        X_train, X_test = train_test_split(X, test_size=0.2, shuffle=False)
        y_train, y_test = train_test_split(y, test_size=0.2, shuffle=False)
        self.__X_train, self.__y_train = self.make_window(X_train,y_train,self.__input_steps,self.__horizon_steps)

        self.__X_test, self.__y_test = self.make_window(X_test,y_test,self.__input_steps,self.__horizon_steps)

    def train(self, epochs : int = 1, batch_size : int = 32):
        if self.__X_train is None or self.__y_train is None:
            self.split()
        es = tf.keras.callbacks.EarlyStopping(monitor='loss', patience = 2)

        X_train, y_train = self.__X_train, self.__y_train

        if self.__model is None:
            return self.create_model()
        model = self.__model
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks = [es])
        return 'done'

    def predict(self):
        X_test = self.__X_test
        preds = []
        for i in range(self.__horizon_steps):
            pred = self.__model.predict(X_test[i:i+1])
            pred = pred.reshape(-1, pred.shape[-1])

            pred = self.__normalizer_used.inverse_transform(pred)

            preds.append(pred[0].astype(float))
            X_test[i + 1, :-1] = X_test[i, 1:]
            X_test[i + 1, -1] = pred[0, 0]
        new_dates = pd.date_range(self.__ts_column.tail(1).values[0], periods=self.__horizon_steps + 1, freq='T')[1:]

        if self.output_fields:
            out = self.output_fields
                                # else the ordering of the input fields would impact the one of the predictions
        else:
            out = self.__df.columns

        rows = []

        for i in range(len(preds)):
            my_dict = dict(list(zip(out,preds[i])))
            my_dict['ts'] = new_dates[i]
            rows.append(my_dict)

        return rows

    def create_model(self, optimizer = 'adam', loss_f = 'huber'):
        if self.output_fields:
            n_features = len(self.output_fields)
        else:
            n_features = len(self.__df.columns)

        if self.input_fields:
            n_input_feats = len(self.input_fields)
        else:
            n_input_feats = len(self.__df.columns)

        self.__optim = optimizer
        self.__loss = loss_f

        input_shape = (self.__input_steps, n_input_feats)
        model = tf.keras.models.Sequential()
        model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(128, return_sequences=False))
        model.add(Dense(self.__horizon_steps * n_features))
        model.add(Reshape([self.__horizon_steps, n_features]))
        model.compile(optimizer=optimizer, loss=loss_f, metrics=['mse'])
        model.build((None, input_shape[0], input_shape[1]))

        self.__model = model

    @property
    def model(self):
        return self.__model
