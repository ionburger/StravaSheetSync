from flask import Flask, request, jsonify, render_template
from event import event
from stravalib import Client
from log import debug
import os
from pymongo import MongoClient

mongo = MongoClient(f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}")
db = mongo["data"]["athletes"]


app = Flask(__name__)

STRAVA_VERIFY_TOKEN = 'stravamoment'

@app.route("/")
def login():
    c = Client()
    url = c.authorization_url(
        client_id=os.environ['STRAVA_ID'],
        redirect_uri="http://localhost:8080/strava-oauth",
        approval_prompt="auto",
    )
    return render_template("login.html", authorize_url=url)


@app.route("/strava-oauth")
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get("error")
    state = request.args.get("state")
    if error:
        return render_template("login_error.html", error=error)
    else:
        code = request.args.get("code")
        client = Client()
        token = client.exchange_code_for_token(
            client_id=os.environ['STRAVA_ID'],
            client_secret=os.environ['STRAVA_SECRET'],
            code=code,
        )
        # Probably here you'd want to store this somewhere -- e.g. in a database.
        strava_athlete = client.get_athlete()

        db.insert_one({
            'id': strava_athlete.id,
            'email': strava_athlete.email,
            'token': token["refresh_token"]
        },
        upsert=True
        )

        return render_template(
            "login_results.html",
            athlete=strava_athlete,
            access_token=access_token
        )


@app.route('/strava', methods=['GET', 'POST'])
def webhook():
    debug('Received webhook')
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == STRAVA_VERIFY_TOKEN:
            return jsonify({'hub.challenge': challenge})
        else:
            return 'Verification token mismatch', 403

    if request.method == 'POST':
        data = request.json
        debug(type(data))
        debug(f'Received event: {data}')
        event(data)
        debug('Event processed')
        return '', 200