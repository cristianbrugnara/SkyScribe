from ..cl_helper_functions import weather_json_to_oop
from datetime import datetime
from client_library.sky_scribe.sample import Sample


def test_weather_json_to_oop_0():
    my_dict = {}
    try:
        result = weather_json_to_oop(my_dict)
    except KeyError as e:
        msg = str(e)

    assert msg == "'ts'"


def test_weather_json_to_oop_1():
    date = datetime(1000,10,1,1,1)

    my_dict = {'ts':date}
    result = weather_json_to_oop(my_dict)

    assert str(result) == str(Sample(date))


def test_weather_json_to_oop_2():
    date = datetime(1000,10,1,1,1)

    my_dict = {'ts':date, 'temperature':3}
    result = weather_json_to_oop(my_dict)

    other = Sample(date, temperature=3)

    assert str(result) == str(other) and result.temperature == other.temperature


def test_weather_json_to_oop_3():
    date = datetime(1000,10,1,1,1)
    temps = [2,10,30]

    my_dict_l = []
    samples = []
    for i in range(len(temps)):
        my_dict_l.append({'ts':date, 'temperature' : temps[i]})
        samples.append(Sample(date,temperature = temps[i]))

    result = weather_json_to_oop(my_dict_l)

    check = True
    # instead of simply checking the single elements in the first loop i want to check that the list is built correctly
    for i in range(len(result)):
        if str(result[i]) != str(samples[i]) or result[i].temperature != samples[i].temperature:
            check=False

    assert check


def test_weather_json_to_oop_4():
    date = datetime(1000, 10, 1, 1, 1)

    my_dict_l = []
    samples = []
    for i in range(3):
        my_dict_l.append({'ts': date})
        samples.append(Sample(date))

    result = weather_json_to_oop(my_dict_l)

    check = True
    for i in range(len(result)):
        if str(result[i]) != str(samples[i]):
            check = False

    assert check