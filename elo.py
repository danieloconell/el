def predict(a, b):
    """ Calculate expected score of A in a match against B.
    A (int): Elo rating for player A.
    B (int): Elo rating for player B.

    Returns:
        Prediction of player A winning.
    """
    return 1 / (1 + 10 ** ((b - a) / 400))


def update(old, exp, score, k=32):
    """ Update the Elo rating for a player.
    old (int): The previous Elo rating.
    exp (int): The expected score for this match.
    score (int): The actual score for this match.
    k (int): The k-factor for Elo (default: 32).

    Returns:
        Players new Elo score.
    """
    return old + k * (score - exp)
