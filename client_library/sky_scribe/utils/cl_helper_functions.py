from typing import List,Dict,Union
from ..sample import Sample
from pandas import DataFrame
from datetime import datetime


def weather_json_to_dataframe(data : Union[List[Dict], Dict], idx : str = None):
    if type(data) == dict:
        res=DataFrame([data])
    else:
        res=DataFrame(data)
    if idx is not None:
        res.set_index(idx,inplace=True)
    return res


def weather_json_to_oop(data : Union[List[Dict], Dict]):
    if type(data) == dict:
        return Sample(data['ts'], **data)

    return [Sample(el['ts'], **el) for el in data]


# put the build_date function here to avoid circular imports between sky_scribe and weather_station
def build_date(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour=hour, minute=minute)
