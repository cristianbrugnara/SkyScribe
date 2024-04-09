from web_service.utils.ws_helper_functions import handle_date
from datetime import datetime


def test_handle_date_0():
    date = handle_date('2003-12-3 11:12:13')
    assert type(date) == datetime


def test_handle_date_1():
    date = handle_date('2003-12-3 11:12:13')
    assert date == datetime(2003,12,3,11,12,13)


def test_handle_date_2():
    msg = ''
    try:
        date = handle_date('2003/12/3 11:12:13')
    except ValueError as e:
        msg = str(e)
    assert msg == "time data '2003/12/3 11:12:13' does not match format '%Y-%m-%d %H:%M:%S'"
