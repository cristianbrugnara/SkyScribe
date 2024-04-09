import pandas as pd
from pandas import DataFrame
from typing import Callable


class BlynkSaver:

    def __init__(self):
        self.__n_dataset = 1

    def blynk_to_tabular(self, blynk_file_path :  str, station_location : str, frequency : str = 'm',
                         df_saving_function : Callable[[DataFrame], None] = None, create_file : bool = False):

        exploring_data = pd.read_csv(blynk_file_path)

        exploring_data.ts = pd.to_datetime(exploring_data.ts, format='ISO8601')

        exploring_data.drop('stringvalue', axis=1, inplace=True)

        unique_pins = exploring_data['pin'].unique()
        unique_pins.sort()


        for pin in unique_pins:
            exploring_data[f'pin_{pin}'] = (exploring_data['pin'] == pin).astype(int)

        exploring_data.drop('pin_30', axis=1, inplace=True) # blynk produced columns

        for p in exploring_data.columns[7:]:
            exploring_data[p] = exploring_data[p] * exploring_data['doublevalue']

        exploring_data.drop(['doublevalue', 'email', 'project_id', 'pin', 'pintype'], axis=1, inplace=True)

        exploring_data.set_index('ts', inplace=True)


        if frequency == 'm':
            df_new = exploring_data.resample('1T').apply(lambda x: x[x != 0].mean() if len(x[x != 0]) > 0 else 0)

        elif frequency == 'h':
            df_new = exploring_data.resample('60min').apply(lambda x: x[x != 0].mean() if len(x[x != 0]) > 0 else 0)

        df_new.rename(columns={'pin_1': 'lightning_distance_km',
                               'pin_2': 'lightning_unknown1',
                               'pin_3': 'lightning_unknown2',
                               'pin_4': 'water_leakage_alarm',
                               'pin_5': 'temp_c',
                               'pin_6': 'humidity',
                               'pin_7': 'wind_max_meter_sec',
                               'pin_8': 'wind_avg_meter_sec',
                               'pin_9': 'wind_direction_deg',
                               'pin_10': 'rain_mm',
                               'pin_11': 'moisture',
                               'pin_12': 'sensor_id',
                               'pin_13': 's_type',
                               'pin_14': 'battery_ok',
                               'pin_15': 'rssi',
                               'pin_16': 'temp_mp1',
                               'pin_17': 'pressure_mp1',
                               'pin_18': 'altitude_mpl',
                               'pin_19': 'voltage_battery',
                               'pin_20': 'mA_battery',
                               'pin_21': 'mA_solar'},
                      inplace=True)

        df_new['location']=station_location

        result_path = f'data_treated_{self.__n_dataset}.csv'

        if df_saving_function:
            df_new['ts'] = df_new.index
            df_saving_function(df_new)

        if create_file or not df_saving_function:
            df_new.to_csv(result_path)

            self.__n_dataset += 1

            return result_path
