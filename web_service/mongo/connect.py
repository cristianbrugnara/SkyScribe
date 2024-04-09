from pymongo import MongoClient
from ..utils.config import MONGO_URL

client = MongoClient(MONGO_URL)

db = client.weather_data

stations = db.stations

station_0 = db.station_0


