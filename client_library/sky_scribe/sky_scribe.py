from __future__ import annotations

import requests
from datetime import datetime
from typing import Dict, List
from .exceptions import NotFoundError,BadRequestError
from .utils.config import URL_BASELINE
from .weather_station import WeatherStation
from .utils.cl_helper_functions import build_date as date_builder


# GENERAL FUNCTIONS

current_stations = None


def get_all_stations_data() -> List[Dict]:
    """
    This function is used to obtain the relevant information of the currently existing weather station connected to the API.
    The information include the station identifier, address and the list of parameters it measures.

    :return: List of dictionaries which contain one station information.
    :rtype: List[Dict]
    """

    return requests.get(f"{URL_BASELINE}/stations/").json()


def get_one_station_data(station_id : int = None, location : str = None) -> Dict:
    """
    This function is used to obtain the data of a specific station based on its ID or location.
    It is a shortcut of the previous function + using its list index.

    :param station_id: The ID associated to the station.
    :param location: The address or city location of the station.
    :return: Returns a dictionary with the station information.
    :rtype: Dict
    """
    if station_id is None and location is None:   # don't use if not station_id because it can be 0
        raise BadRequestError('You must insert either the ID or the location of the station.')

    if location:
        loc = {'location' : location}
        return requests.get(f"{URL_BASELINE}/stations", json=loc).json()

    if station_id is not None:
        station_id = str(station_id)

    return requests.get(f"{URL_BASELINE}/stations/{station_id}").json()


def get_one_station(station_id: int) -> WeatherStation:
    """
    Used to access the object to interact with a specific weather station by specifying its ID, it automatically finds the station location and uses it.
    :param station_id: The ID associated to the station.
    :return: Instance of :class: WeatherStation.
    :rtype: WeatherStation
    """

    if station_id is None:  # don't use if not station_id because it can be 0
        raise BadRequestError('You must insert the ID of the station.')

    my_list = get_all_stations_data()
    station_location = None
    for el in my_list:
        if el['_id'] == station_id:
            station_location = el['location']
    if not station_location:
        raise NotFoundError("The station doesn't exist.")

    return WeatherStation(station_id, station_location)


def build_date(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    """
    Helper function that creates a date to be used with the other functions. It is also possible to use normal `datetime` functions.
    :type year: int
    :type month: int
    :type day: int
    :type hour: int
    :type minute: int
    :return: A datetime object.
    :rtype: datetime
    """
    return date_builder(year,month,day,hour,minute)




