from flask import Flask, request, jsonify
from event import event
from stravalib import Client
from log import debug

app = Flask(__name__)

STRAVA_VERIFY_TOKEN = 'stravamoment'

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