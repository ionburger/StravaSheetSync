from stravalib.client import Client
from log import debug
from pymongo import MongoClient
import os

mongo = MongoClient(f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}")
db = mongo["data"]["athletes"]
strava = Client()



def event(data):
    Client.refresh_access_token()
    activity = client.get_activity(data['object_id'])
    debug(activity)
