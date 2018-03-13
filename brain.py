from elo import El
from data import Store
from pprint import pprint


class Brain:
    el = El(32)
    store = Store([2018])

    scores = {}

    predictions = {}

    def __init__(self):
        self.default_score = 0
        self.run_past_matches()

    def run_past_matches(self):
        print(self.store.years)
        for year in self.store.years:
            print(year)
            for match in self.store.matches[year]:
                print(match)
                red_alliance = match["red_alliance"]
                blue_alliance = match["blue_alliance"]

                for team in red_alliance + blue_alliance:
                    if team not in self.scores.keys():
                        self.scores[team] = self.default_score

            prediction = self.predict(red_alliance, blue_alliance,
                                      key=match["key"])
            self.update_score(red_alliance, blue_alliance, prediction,
                              match["red_score"], match["blue_score"])

    def predict(self, red_alliance, blue_alliance, key=False):
        red_score = sum([self.scores[team] for team in red_alliance])
        blue_score = sum([self.scores[team] for team in blue_alliance])

        score = self.el.predict(red_score, blue_score)

        if key:
            self.predictions[key] = score

        return score

    def update_score(self, red_alliance, blue_alliance, prediction, red_score, blue_score):
        score = self.get_score(red_score, blue_score)

        for team in red_alliance:
            self.scores[team] = self.el.update(self.scores[team], prediction,
                                               score)

        for team in blue_alliance:
            self.scores[team] = self.el.update(self.scores[team],
                                               1 - prediction, score)

    def get_score(self, red_score, blue_score):
        if red_score - blue_score > 0:
            return 1
        elif red_score - blue_score < 0:
            return 0
        elif red_score == blue_score:
            return 0.5
        # return red_score / (red_score + blue_score)
        return None


if __name__ == "__main__":
    a = Brain()
    pprint(a.scores)
