from blynk_saver import BlynkSaver
import pandas as pd
from insert_into_database import DatabaseSaver

saver = BlynkSaver()
saver.blynk_to_tabular("../datasets/blynk.csv", 'Lugano',
                              frequency='m', df_saving_function=None)


df = pd.read_csv('data_treated_1.csv')[19068:]  # the first half of the data was missing or unreliable

df.drop(['sensor_id','lightning_distance_km',
         'lightning_unknown1','lightning_unknown2','water_leakage_alarm','moisture',
         's_type'], axis=1, inplace=True)

df['ts'] = pd.to_datetime(df['ts'], format='%Y-%m-%d %H:%M:%S')
DatabaseSaver.save_data_from_dataframe(df)