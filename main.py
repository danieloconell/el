from brain import Brain
from flask import Flask, request

app = Flask(__name__)
brain = Brain()


@app.route("/")
def home():
    return 'Wow'


@app.route("/api/predict/<red_alliance>/<blue_alliance>")
def predict(red_alliance, blue_alliance):
    return str(brain.predict(red_alliance, blue_alliance)), {'Content-Type': 'text/plain'}


@app.route('/tba-webhook', methods=['POST'])
def tba_webhook():
    msg_data = request.json['message_data']
    msg_type = request.json['message_type']
    if msg_type == 'verification':
        print('TBA verification key: %s' % msg_data)
    if msg_type == 'ping':
        print('Just been pinged by The Blue Alliance.')
    elif msg_type == 'upcoming_match':
        brain.predict(msg_data["team_keys"][:3], msg_data["team_keys"][3:], key=msg_data["match_key"])
    elif msg_type == 'match_score':
        red_alliance = msg_data["alliances"]["red"]["teams"]
        blue_alliance = msg_data["alliances"]["blue"]["teams"]
        red_score = msg_data["alliances"]["red"]["score"]
        blue_score = msg_data["alliances"]["blue"]["score"]

        if red_score - blue_score > 0:
            score = 1
        elif red_score - blue_score < 0:
            score = 0
        elif red_score - blue_score == 0:
            score = 0.5

        if brain.predictions[msg_data["match"]["key"]] in brain.predictions.keys():
            predict_score = brain.predictions[msg_data["match"]["key"]]
        else:
            predict_score = brain.predict(red_alliance, blue_alliance)

        brain.update_score(red_alliance, blue_alliance, score, predict_score)
