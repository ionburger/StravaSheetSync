from flask import Flask, request, jsonify
from event import Event


app = Flask(__name__)

STRAVA_VERIFY_TOKEN = 'stravamoment'

@app.route('/strava', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == STRAVA_VERIFY_TOKEN:
            return jsonify({'hub.challenge': challenge})
        else:
            return 'Verification token mismatch', 403

    if request.method == 'POST':
        data = request.json
        print(f'Received event: {event}')
        Event(data)
        return '', 200

if __name__ == '__main__':
    app.run(port=8080)
