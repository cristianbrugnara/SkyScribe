from web_service.classes.weather_station.weather_station import WeatherStation
from typing import Union, Dict
from .existing_stations import station_menu
from web_service.mongo.connect import stations
from datetime import datetime


def find_station(id_or_loc: Union[int,str]) -> Union[WeatherStation, None]:
    try:
        my_id=int(id_or_loc)  # if by id

    except ValueError:   # if by location
        my_id = int(stations.find_one({'location' : id_or_loc.title()})['_id'])

    if my_id in station_menu.keys():
        return station_menu[my_id]
    return None


def handle_date(string_date : str):
    return datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')


class MongoFilterer:
    def __init__(self,  query_dict : Dict):
        self.__data = query_dict
        self.__operators = {">" : "$gt",
                            "<" : "$lt",
                            ">=" : "$gte",
                            "<=" : "$lte",
                            "=" : "$eq"}

    def __str__(self):
        return f"Now working on the following dictionary (obtained from a query string): {self.__data}. " \
               f"Reminder on the available operators: {self.__operators}"

    def filter_by_key(self, key : str):
        filters = self.__data[key]
        apply_filters = {}

        for f in filters:
            operator = ""
            new_operator = None
            value = ""

            for char in f:

                if char in '><=':
                    operator+=char

                else:
                    if not new_operator:
                        new_operator = self.__operators[operator]
                    value+=char

            apply_filters[new_operator] = float(value)

        return apply_filters

