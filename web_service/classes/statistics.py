import pandas as pd

class Statistics:
    def __init__(self, id_station, start_time, end_time):
        self.__id_station = id_station
        self.__start_time = start_time
        self.__end_time = end_time

    def read_csv(self, name_file: str):
        df = pd.read_csv(f'./../dataset_treatment/{name_file}')
        return df
