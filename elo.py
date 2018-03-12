class El:

    def __init__(self, k=32):
        self.k = k

    def predict(self, a, b):
        """ Calculate expected score of A in a match against B.
        A (int): Elo rating for player A.
        B (int): Elo rating for player B.

        Returns:
            Prediction of player A winning.
        """
        return 1 / (1 + 10 ** ((b - a) / 400))

    def update(self, old, exp, score):
        """ Update the Elo rating for a player.
        old (int)   : The previous Elo rating.
        exp (int): The expected score for this match.
        score (int): The actual score for this match.

        Returns:
            Players new Elo score.
        """
        return old + self.k * (score - exp)
