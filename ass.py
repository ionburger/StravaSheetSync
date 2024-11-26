from stravalib import Client
from dotenv import load_dotenv
import os
load_dotenv()


client = Client()
url = client.authorization_url(
    client_id=os.getenv("CLIENT_ID"),
    redirect_uri="http://localhost:5000/authorization",
)
print(url)
token_response = client.exchange_code_for_token(
    client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), code=os.getenv("CODE")
)
access_token = token_response["access_token"]
refresh_token = token_response["refresh_token"]
print(refresh_token)