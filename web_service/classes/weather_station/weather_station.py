import datetime
from .weather_station_data import WeatherData
from web_service.mongo.connect import db
from client_library.sky_scribe.sample import Sample
from web_service.classes.time_series.forecaster import Forecaster
from typing import List


class WeatherStation(WeatherData):
    def __init__(self, id: int):
        self.__id=id
        self.__loc=db.stations.find_one({'_id': id})['location']
        WeatherData.__init__(self, db[f'station_{id}'])
        self.__models = []

    @property
    def id(self):
        return self.__id

    @property
    def location(self):
        return self.__loc

    @property
    def models(self):
        return self.__models

    def __str__(self):
        return f"Weather station | ID: {self.id} | City: {self.location}"

    def add_measurement(self, date: datetime, temp_c : float =0, humidity : float =0,wind_max_meter_sec : float = 0,
                                   wind_direction_deg : float =0,wind_avg_meter_sec :float = 0,rain_mm : float =0,battery_ok : float =0,
                                   rssi : float =0, temp_mp1 : float =0, pressure_mp1 : float =0,altitude_mpl : float =0,
                                   voltage_battery : float =0, mA_battery : float =0, mA_solar : float =0,**params):

        new_sample = Sample(date,temp_c=temp_c, humidity=humidity, wind_max_meter_sec=wind_max_meter_sec, wind_avg_meter_sec=wind_avg_meter_sec
                                   ,wind_direction_deg=wind_direction_deg,rain_mm =rain_mm,battery_ok=battery_ok,
                                   rssi=rssi, temp_mp1=temp_mp1, pressure_mp1=pressure_mp1,altitude_mpl=altitude_mpl,
                                   voltage_battery=voltage_battery, mA_battery =mA_battery, mA_solar=mA_solar, **params)

        result = WeatherData.add_measurement(self,new_sample)

        if date < self.start:
            self.update_oldest_date()

        if date > self.end:
            self.update_newest_date()

        return result

    def update_measurement_by_date(self, date: datetime, temp_c : float =0, humidity : float =0,wind_max_meter_sec : float = 0,
                                   wind_direction_deg : float =0,wind_avg_meter_sec :float = 0,rain_mm : float =0,battery_ok : float =0,
                                   rssi : float =0, temp_mp1 : float =0, pressure_mp1 : float =0,altitude_mpl : float =0,
                                   voltage_battery : float =0, mA_battery : float =0, mA_solar : float =0,**params):

        new_sample = Sample(date,temp_c=temp_c, humidity=humidity,wind_max_meter_sec=wind_max_meter_sec,wind_avg_meter_sec=wind_avg_meter_sec
                                   ,wind_direction_deg=wind_direction_deg,rain_mm =rain_mm,battery_ok=battery_ok,
                                   rssi=rssi, temp_mp1=temp_mp1, pressure_mp1=pressure_mp1,altitude_mpl=altitude_mpl,
                                   voltage_battery=voltage_battery, mA_battery =mA_battery, mA_solar=mA_solar, **params)

        result = WeatherData.update_measurement_by_date(self,new_sample)
        if not result:
            return None

        if new_sample.ts < self.start:
            self.update_oldest_date()

        if new_sample.ts > self.end:
            self.update_newest_date()
        return 'ok'

    def mean(self, pin: str, start_date: datetime = None, end_date: datetime = None, pretty=False):
        stat = WeatherData.mean(self,pin,start_date,end_date)
        if pretty:
            return f'The mean {pin} of the station {self.__id} in {self.__loc} is: ' \
               f'{stat}'
        return stat

    def max(self, pin: str, start_date: datetime = None, end_date: datetime = None, pretty=False):
        stat = WeatherData.max(self, pin, start_date, end_date)
        if pretty:
            return f'The mean {pin} of the station {self.__id} in {self.__loc} is: ' \
                   f'{stat}'
        return stat

    def min(self, pin: str, start_date: datetime = None, end_date: datetime = None, pretty=False):
        stat = WeatherData.min(self, pin, start_date, end_date)
        if pretty:
            return f'The mean {pin} of the station {self.__id} in {self.__loc} is: ' \
                   f'{stat}'
        return stat

    def std(self, pin: str, start_date: datetime = None, end_date: datetime = None, pretty=False):
        stat = WeatherData.std(self, pin, start_date, end_date)
        if pretty:
            return f'The mean {pin} of the station {self.__id} in {self.__loc} is: ' \
                   f'{stat}'
        return stat

    def create_model(self, input_fields : List[str] = None, output_fields : List[str] = None,
                     input_steps = 300,horizon_steps : int = 250,
                              optimizer = 'adam', loss = 'huber'):
        forecast = Forecaster(self.id, input_fields, output_fields,input_steps,horizon_steps)

        if input_fields is None:
            n = len(db.stations.find_one({"_id" : self.id})['available_data'])

        else:
            n = len(input_fields)

        forecast.create_model(optimizer, loss)

        self.__models.append(forecast)
        idx = len(self.__models)-1

        self.__horizon = horizon_steps

        return idx

    def delete_model(self, idx : int):
        self.models.pop(idx)

    def update_model(self, idx : int, input_fields = None, output_fields = None):
        self.models[idx].update_data(input_fields, output_fields)

    def train_model(self, idx : int,epochs : int = 1,batch_size : int = 32):
        return self.models[idx].train(epochs,batch_size)

    def predict(self, idx : int,):
        return self.__models[idx].predict()
