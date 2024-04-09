from client_library.sky_scribe.utils.cl_helper_functions import weather_json_to_dataframe
from pandas import DataFrame


def test_weather_json_to_dataframe_0():
    my_dict = {'temperature' : 400, 'rain_mm' : 0.2}
    result = weather_json_to_dataframe(my_dict)

    assert result.equals(DataFrame.from_dict([my_dict]))


def test_weather_json_to_dataframe_1():
    my_dict = {'index' :0, 'rain_mm' : 0.2}
    result = weather_json_to_dataframe(my_dict,idx='index')

    df = DataFrame.from_dict([my_dict])
    df.set_index('index', inplace=True)

    assert result.equals(df)


def test_weather_json_to_dataframe_2():
    my_dict = {}
    result = weather_json_to_dataframe(my_dict)

    assert result.empty


def test_weather_json_to_dataframe_3():
    my_dict_l = [{'temperature': 2, 'rain_mm': 0.2},
                 {'temperature': 10, 'rain_mm': 0.23},
                 {'temperature': 30, 'rain_mm': 0.7}]
    result = weather_json_to_dataframe(my_dict_l)

    assert result.equals(DataFrame.from_dict(my_dict_l))


def test_weather_json_to_dataframe_4():
    my_dict_l = [{'index':0, 'temperature': 2, 'rain_mm': 0.2},
                 {'index':1, 'temperature': 10, 'rain_mm': 0.23},
                 {'index':2, 'temperature': 30, 'rain_mm': 0.7}]
    result = weather_json_to_dataframe(my_dict_l,idx='index')

    df = DataFrame.from_dict(my_dict_l)
    df.set_index('index',inplace=True)

    assert result.equals(df)


def test_weather_json_to_dataframe_5():
    my_dict_l = []
    result = weather_json_to_dataframe(my_dict_l)

    assert result.empty


def test_weather_json_to_dataframe_6():
    my_dict_l = [{}, {}]
    result = weather_json_to_dataframe(my_dict_l)

    assert result.empty
