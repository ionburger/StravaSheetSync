from stravalib.client import Client
from log import debug
from pymongo import MongoClient

mongo = MongoClient()
db = mongo["data"]["athletes"]
strava = Client()



def event(data):
    Client.refresh_access_token()
    activity = client.get_activity(data['object_id'])
    debug(activity)
