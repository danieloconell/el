from brain import Brain
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path="/static")
brain = Brain()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/team/<int:team>")
def team(team):
    return render_template("team.html", content="",
                           name=team)


@app.route("/event/<string:event>")
def event(event):
    return render_template("event.html", content=event(event),
                           name=event)


@app.route("/year/<int:year>")
def year(year):
    return render_template("year.html", content=year(year),
                           name=year)


@app.route("/api/predict/<red_alliance>/<blue_alliance>")
def predict(red_alliance, blue_alliance):
    return str(brain.predict(red_alliance, blue_alliance)), \
            {'Content-Type': 'text/plain'}


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
        if brain.predictions[msg_data["match"]["key"]] in brain.predictions.keys():
            predict_score = brain.predictions[msg_data["match"]["key"]]
        else:
            predict_score = brain.predict(red_alliance, blue_alliance)

        brain.update_score(red_alliance, blue_alliance, predict_score,
                           red_score, blue_score)


if __name__ == "__main__":
    app.run()
