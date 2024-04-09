from typing import Any, Dict, Tuple
from datetime import datetime
from abc import ABC
from pandas.plotting._matplotlib import LinePlot
from pymongo.collection import Collection
from client_library.sky_scribe.sample import Sample
from web_service.classes.statistics.statistics import Statistics
from web_service.classes.graphs.boxplot import Boxplot
from web_service.classes.graphs.scatterplot import ScatterPlot
from web_service.classes.graphs.histogram import Histogram
from web_service.classes.graphs.lineplot import LinePlot


# handles a mongo collection referred to a single station

class WeatherData(ABC):
    def __init__(self, data: Collection):
        self.__data = data
        self.update_oldest_date()
        self.update_newest_date()

        self.__dates_used = [el['ts'] for el in self.data.find({},{'ts':1})]

    def update_oldest_date(self):
        self.__start =  self.data.find({},{'ts':1}).sort('ts').limit(1)[0]['ts']

    def update_newest_date(self):
        self.__end = self.data.find({},{'ts':1}).sort({'ts': -1}).limit(1)[0]['ts']

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def data(self):
        return self.__data

    def add_measurement(self, data : Sample):
        data_dict = data.__dict__
        if '_modifiable' in data_dict.keys():
            data_dict.pop('_modifiable')

        if data_dict['ts'] not in self.__dates_used:
            self.data.insert_one(data_dict)
            self.__dates_used.append(data_dict['ts'])
        else:
            return 400

    def get_measurement_by_date(self,date: datetime, which_fields: Dict = {'_id': 0}):
        my_dict=self.data.find_one({'ts' : date}, which_fields)
        if not my_dict:
            return None
        return my_dict

    def get_measurements_by_date_range(self, start_date : datetime = None, end_date : datetime = None,
                                       which_fields: Dict = {'_id': 0}):
        if not start_date:
            start_date = self.__start
        if not end_date:
            end_date = self.__end

        data = list(self.data.find({
            'ts' : {
                "$gte" : start_date,
                "$lte" : end_date}},
            which_fields).sort('ts'))
        if len(data) == 0:
            return None

        return data

    def get_measurement_mongo_filtered(self, mongo_filter : Dict, which_fields: Dict = {'_id': 0}):
        data = list(self.data.find(mongo_filter, which_fields).sort('ts'))
        if len(data) == 0:
            return None

        return data

    def update_measurement_field_by_date(self, date: datetime, value : Any, field: str):  # changes one parameter
        result = self.data.update_one({'ts' : date}, {"$set" : {f"{field}" : value}})
        if result.matched_count == 0:
            return None

        if field == 'ts':
            if value < self.start:
                self.update_oldest_date()

            if value > self.end:
                self.update_newest_date()

        return 200

    def update_measurement_by_date(self, new_sample: Sample): # replace an entire document with another
        data_dict = new_sample.__dict__
        if '_modifiable' in data_dict.keys():
            data_dict.pop('_modifiable')

        result = self.data.replace_one({'ts' : new_sample.ts},data_dict)

        if result.matched_count == 0:
            return None

        return 200

    def delete_sample_by_date(self, date: datetime):
        result = self.data.delete_one({'ts': date})

        if result.deleted_count == 0:
            return None

        if date == self.start:
            self.update_oldest_date()
        if date == self.end:
            self.update_newest_date()
        self.__dates_used.remove(date)
        return 200

    def _get_feature_array(self, pin, start_date: datetime = None, end_date: datetime = None):
        if not start_date:
            start_date = self.__start
        if not end_date:
            end_date = self.__end

        data = self.get_measurements_by_date_range(start_date, end_date,
                                                   which_fields={f"{pin}" : 1, '_id' : 0})
        try:
            feature_array = [el[pin] for el in data]
        except KeyError:
            return None

        return feature_array

    def mean(self, pin: str, start_date: datetime = None, end_date: datetime = None):
        feature_array = self._get_feature_array(pin, start_date, end_date)
        if not feature_array:
            return None

        return Statistics.get_mean(feature_array)

    def max(self, pin: str, start_date: datetime = None, end_date: datetime = None):
        feature_array = self._get_feature_array(pin, start_date, end_date)
        if not feature_array:
            return None

        return Statistics.get_max(feature_array)

    def min(self, pin: str, start_date: datetime = None, end_date: datetime = None):
        feature_array = self._get_feature_array(pin, start_date, end_date)
        if not feature_array:
            return None

        return Statistics.get_min(feature_array)

    def std(self, pin: str, start_date: datetime = None, end_date: datetime = None):
        feature_array = self._get_feature_array(pin, start_date, end_date)
        if not feature_array:
            return None

        return Statistics.get_std(feature_array)

    def box_plot(self, pin: str, figsize: Tuple[int ,int] = (10, 10)):
        array = self._get_feature_array(pin)

        return Boxplot(array, pin, figsize).plot_graph()

    def scatter_plot(self, pin1: str, pin2: str, figsize: Tuple[int ,int] = (10, 10)):

        array1 = self._get_feature_array(pin1)
        array2 = self._get_feature_array(pin2)

        return ScatterPlot(array1, array2, pin1, pin2, figsize).plot_graph()

    def line_plot(self, pin1: str, pin3: str=None, figsize:Tuple[int ,int] = (10, 10)):
        array1 = self._get_feature_array(pin1)
        pin2 = "ts"
        array2 = self._get_feature_array(pin2)

        if pin3 is not None:
            array3 = self._get_feature_array(pin3)

            return LinePlot(array1, array2, pin1, pin2, pin3, array3, figsize)

        return LinePlot(array1, array2, pin1, pin2, figsize)

    def histogram(self, pin: str, figsize: Tuple[int ,int] = (10, 10)):
        array = self._get_feature_array(pin)

        return Histogram(array, pin, figsize).plot_graph()

