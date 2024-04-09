from web_service.utils.ws_helper_functions import find_station
from web_service.classes.weather_station.weather_station import WeatherStation


def test_find_station_0():
    s = find_station(0)
    assert type(s) == WeatherStation


def test_find_station_1():
    s = find_station(0)
    assert s.id == 0 and s.location.lower() == 'lugano'


def test_find_station_2():
    s = find_station('lugano')
    assert s.id == 0 and s.location.lower() == 'lugano'


def test_find_station_3():
    s = find_station(200)
    assert s is None
