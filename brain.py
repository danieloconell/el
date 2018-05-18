from elo import El
from data import Store
from pprint import pprint


class Brain:
    el = El(32)
    store = Store(range(2008, 2019))

    scores = {}

    predictions = {}

    def __init__(self):
        """Create the Brain class to perform predictions."""
        self.default_score = 1500
        self.run_past_matches()

    def run_past_matches(self):
        """Iterate through matches in Store and calculate Elo rating for teams."""
        for year in self.store.years:
            # print(year)
            for event in self.store.events[year]:
                for match in self.store.matches[year][event.key]:
                    red_alliance = match.red_alliance
                    blue_alliance = match.blue_alliance

                    for team in red_alliance + blue_alliance:
                        if team not in self.scores.keys():
                            self.scores[team] = self.default_score

                    prediction = self.predict(red_alliance, blue_alliance, key=match.key)
                    self.update_score(red_alliance, blue_alliance, prediction,
                                      match.red_score, match.blue_score)

    def predict(self, red_alliance, blue_alliance, key=False):
        """Predict the winner of an FRC game.

        Args:
            red_alliance (list): Teams in red alliance.
            blue_alliance (list): Teams in blue alliance.

        Returns:
            The predicted score of match, 0 = loss etc.
        """
        red_score = sum([self.scores[team] for team in red_alliance])
        blue_score = sum([self.scores[team] for team in blue_alliance])
        score = self.el.predict(red_score, blue_score)

        if key:
            self.predictions[key] = score

        return score

    def update_score(self, red_alliance, blue_alliance, prediction, red_score, blue_score):
        """Update the Elo rating of teams in an alliance.

        Args:
            red_alliance (list): Teams in the red alliance.
            blue_alliance (list): Teams in the blue alliance.
            prediction (int): Predicted score of red alliance.
            red_score (int): Actual score of red alliance.
            blue_score (int): Actual score of blue alliance.
        """
        score = self.get_score(red_score, blue_score)

        for team in red_alliance:
            self.scores[team] = self.el.update(self.scores[team], prediction, score)

        for team in blue_alliance:
            self.scores[team] = self.el.update(self.scores[team], 1 - prediction, score)

    def get_score(self, red_score, blue_score):
        """Return the score of match to be used in prediction. 0 = loss, 1 = win.
        Args:
            red_score (int): Points scored by red alliance.
            blue_score (int): Points score by blue alliance.
        """
        if red_score < blue_score:
            return 0
        elif red_score > blue_score:
            return 1
        else:
            return 0.5


if __name__ == "__main__":
    a = Brain()
    # pprint(a.scores)
