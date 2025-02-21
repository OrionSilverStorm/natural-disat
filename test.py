# this was made to test the map selection code to ensure it woked as intended
import random
import json

data = json.load(open("data.json", "r"))

def getDisaster(map):
    # set the disaster ============================================================================================================================

    # create a dictionary of "disaster name": "relative probability"
    probabilities = {}
    for name in data["disasters"]:
        # get the name of each disaster
        # set it's probability to 1
        probabilities.update({name: 1})

    # get name of each disaster with a specified probability within the map object
    for name in map["RelativeDisasterProbabilities"]:
        # update the dictionary with the new probability
        probabilities.update({name: map["RelativeDisasterProbabilities"][name]})

    # make the probabilites cumulative
    total = 0
    for i in probabilities:
        # iterate over dictionary keys
        total += probabilities[i]
        probabilities.update({i: total})

    # chose a random number between 0 and the total
    num = random.uniform(0, total)
    # remove disasters from the probabilites dictionary who's probability is < the random num
    temp = {}
    for i in probabilities:
        if probabilities[i] > num:
            temp.update({i: probabilities[i]})
    probabilities = temp

    # get the key of the value with the lowest probability
    temp = min(probabilities.values())
    disaster = [key for key in probabilities if probabilities[key] == temp][0]
    
    return disaster

for map in list(data["maps"].items()):
    map = {"name": map[0], "RelativeDisasterProbabilities": map[1]["RelativeDisasterProbabilities"]}
    
    results = {}
    for name in data["disasters"]:
        results.update({name: 0})
        
    for i in range(100000):
        disaster = getDisaster(map)
        results.update({disaster: results[disaster] + 1})
    
    print(f"{map["name"]}:")
    print(results)