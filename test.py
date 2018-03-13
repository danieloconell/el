from brain import Brain

brain = Brain()

results = []
results1 = []

for match in brain.store.years[2017]:
    a = brain.predict(match["red_alliance"], match["blue_alliance"])
    if a >= 0.5 and match["score"] >= 0.5:
        results.append(True)
    elif a < 0.5 and match["score"] < 0.5:
        results.append(True)
    else:
        results.append(False)

    results1.append(match["score"] - a)** 2 )

print(str(round(results.count(True) / len(results)*100, 2)) + "%")
print("Brier:")
print(sum(results1)/len(results1))
