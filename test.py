from brain import Brain

brain = Brain()

results = []
for match in brain.store.matches[2018]:
    a = brain.predict(match["red_alliance"], match["blue_alliance"])

    score = brain.get_score(match["red_score"], match["blue_score"])

    results.append((score - a) ** 2)

brier_score = (sum(results)/len(results))

print(results.count(True)/ len(results))
print("Brier:")
print(1-brier_score**(1/2))
print(brier_score)