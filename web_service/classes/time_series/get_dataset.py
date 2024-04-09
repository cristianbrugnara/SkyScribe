from web_service.mongo.connect import db
import pandas as pd
from typing import Dict, Union


def mongo_to_dataframe(station_id : int, which_fields : Union[Dict,'all'] = 'all'):
    if which_fields == 'all':
        data = db[f'station_{station_id}'].find().sort('ts')
    else:
        which_fields['ts'] = 1
        data = db[f'station_{station_id}'].find({}, which_fields).sort('ts')
    df = pd.DataFrame(data).drop('_id', axis=1)

    return df
