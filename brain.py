from elo import El
from data import Store
from tqdm import tqdm
from pprint import pprint

class Brain:
    el = El(32)
    store = Store([2018, 2017, 2016])

    scores = {}

    predictions = {}

    def __init__(self):       
        self.default_score = 0
        self.run_past_matches()

    def run_past_matches(self):
        for match in tqdm(self.store.matches):
            red_alliance = match["red_alliance"]
            blue_alliance = match["blue_alliance"]

            for team in red_alliance + blue_alliance:
                if team not in self.scores.keys():
                    self.scores[team] = self.default_score

            prediction = self.predict(red_alliance, blue_alliance, key=match["key"])
            self.update_score(red_alliance, blue_alliance, prediction, match["score"])

    def predict(self, red_alliance, blue_alliance, key=False):
        red_score = sum([self.scores[team] for team in red_alliance]) / 3
        blue_score = sum([self.scores[team] for team in blue_alliance]) / 3

        score = self.el.predict(red_score, blue_score)

        if key:
            self.predictions[key] = score

        return score

    def update_score(self, red_alliance, blue_alliance, prediction, score):
        for team in red_alliance:
            self.scores[team] = self.el.update(self.scores[team], prediction, score)

        for team in blue_alliance:
            self.scores[team] = self.el.update(self.scores[team], 1 - prediction, score)

if __name__ == "__main__":
    a = Brain()
    pprint(a.scores)
    print(a.predict(["frc4817", "frc3008", "frc4802"], ["frc6836", "frc6083", "frc4253"]))
