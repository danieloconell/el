from brain import Brain

brain = Brain()

results = []
results1 = []
print()
for match in brain.store.matches[2018]:
    a = brain.predict(match["red_alliance"], match["blue_alliance"])

    score = brain.get_score(match["red_score"], match["blue_score"])

    if a >= 0.5 and score >= 0.5:
        results.append(True)
    elif a < 0.5 and score < 0.5:
        results.append(True)
    else:
        results.append(False)

    results1.append((score - a) ** 2)

print(str(round(results.count(True) / len(results)*100, 2)) + "%")
print("Brier:")
print(sum(results1)/len(results1))
