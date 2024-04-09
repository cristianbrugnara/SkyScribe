from pandas import DataFrame
from .connect import db, stations
from typing import Iterable


def samples_from_df(df : DataFrame, station : int):
    db[f'station_{station}'].insert_many(df.to_dict('records'))


def insert_station(number : int, location : str, available_data : Iterable[str]):
    stations.insert_one({'_id' : int(number), 'location' : location, 'available_data' : list(available_data)})
                                # mongo doesn't accept np.int64
