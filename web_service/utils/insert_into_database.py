import pandas as pd
from web_service.mongo.insert_data import samples_from_df, insert_station


class DatabaseSaver:
    @staticmethod   # if we already have a well-formatted (not blynk layout) CSV file
    def save_data_from_csv(file_path, delimiter=','):
        data = pd.read_csv(file_path, delimiter=delimiter)
        data.ts = pd.to_datetime(data.ts, format='%Y-%m-%d %H:%M:%S')

        DatabaseSaver.save_data_from_dataframe(data)

    @staticmethod
    def save_data_from_dataframe(df):
        for id in df['device_id'].unique():
            id = int(id)
            stat_data = df[df['device_id']==id]

            samples_from_df(stat_data.drop(['device_id','location'], axis = 1), station=id)
            cols=[]
            for col in stat_data.columns:
                if col not in ['device_id','ts','location']:
                    cols.append(col)

            insert_station(id, stat_data.location.unique()[0], cols)