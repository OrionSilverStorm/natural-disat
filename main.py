import random
import json
from colours import *

class Player: pass # stops python complaining about type hinting
class Player:
    def __init__(self, name: str, alignment: str) -> None:
        # create a player with a name and alignment
        self.name = name
        self.alignment = alignment
    
    def __str__(self):
        # tell python how to turn a Player object into a string
        return f"{self.name} the {self.alignment}"
    
    def action(self) -> None:
        # make a single player (the calling object) do an action
        print(f"{self.name} {random.choice(data["actions"][self.alignment])}")
    
    def socialise(self, other: Player) -> None:
        # make a player (the calling object) socialise with another player (the "other" object)
        if self == other:
            # if it is the same player, do a hallucination
            print(f"{self.name} {random.choice(data["hallucinations"])}")
        else:
            # otherwise, do a normal social interaction
            print(f"{self.name} {random.choice(data["socailInteractions"])} {other.name}")
    
    def kill(self, other: Player) -> None:
        # the calling object is killed by another player
        if self == other:
            # if it is the same player, do a sucide
            print(f"{self.name} {random.choice(data["suicides"])}")
        else:
            # calling player is killed by another player
            print(f"{self.name} {random.choice(data["socailDeaths"])} {other.name}")
        
        # remove the other playe from the list of players
        # other is always killed, even if self = other
        players.remove(self)
    
    def disasterEfect(self) -> None:
        # check if the disaster is revealed
        if diseasterRevealed:
            # kill someone with the disaster specific deaths
            print(f"{self.name} {random.choice(disaster["deaths"])}")
            players.remove(self)
        else:
            # show sign of disaster
            print(f"{self.name} {random.choice(disaster["warnings"])}")

# initialise the game =========================================================================================================================
#open json file
data = json.load(open("data.json", "r"))

# creates player objects based on json data
players = [Player(i["name"], i["alignment"]) for i in data["players"]] # alive players
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#          creates player object for each entry in the json list

allPlayers = players.copy() # all players that have ever existed, used with /revive and /create
#                   ^^^^^^^
# use .copy() because by default it is only copied by reference

# randomly choose current map
map = random.choice(list(data["maps"].items()))
# turn the map back into a dictionary
map = {"name": map[0], "RelativeDisasterProbabilities": map[1]["RelativeDisasterProbabilities"]}


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
disasterName = [key for key in probabilities if probabilities[key] == temp][0]
disaster = data["disasters"][disasterName]
disaster.update({"name": disasterName})
pass
    
    


# main game loop ==============================================================================================================================
diseasterRevealed = False
print("WELCOME TO YOUR DOOM - NATURAL DISASTER SIMULATOR\n ")

# get extra players
contInput = True
while contInput:
    # get a player name from the user
    playerName = str(input("Enter extra Player name (Enter to skip entering extra people): "))

    # if the user enters nothing, stop asking for more players
    if playerName == "":
        contInput = False
        
    else:
        # attempt to add a new player
        inputValid = False
        while not inputValid:
            # try to get the player's alignment
            try:
                # get user input
                alignment = int(input("\nWhat is you goal? (1 to hide, 2 to explore, 3 to rampage): "))
            except ValueError:
                # user entered something that is not a number
                print("Please be aware of the existence of numbers and/or proper literacy, kindly retry")
            else:
                # user entered a number
                if 1 <= alignment <= 3:
                    # user entered a valid number
                    inputValid = True
                else:
                    # user entered a number that is not in the valid range
                    print("Wrong range of values")
        
        # add the player to the list of players and list of all players
        allPlayers.append(Player(playerName, ["hider", "explorer", "fighter"][alignment-1]))
        players.append(Player(playerName, ["hider", "explorer", "fighter"][alignment-1]))
        #                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # this is a list of the possible alignments, and the user's input is used to choose one of them
        # we subtract 1 from the alignment because the list is 0-indexed, but the user's input is 1-indexed
        # this makes sure the new player object has the correct alignment
del playerName


print(f"\nSite:{map["name"]}\nDisaster Unkown\n")

gameWon = False
while not gameWon:
    userInput = input()

    if userInput == "":
        # if no command is entered, continue the game

        if len(players) == 1:
            # check if there is only one player left
            # if there is print the winner and stop the game
            print(f"THE SOLE SURVIVER OF THE DISEASTER: {disaster["name"]} IN {map["name"]}\nWINNER:{players[0]}")
            gameWon = True
            
        else:
            #ChooseAction(diseasterRevealed)
            # chech if disaster is revealed and if not maybe reveal it
            if not diseasterRevealed and (random.randint(0,100) > 95 or len(players) < 5):
                #if rng or player list is low
                print(f"DISEASTER HAS STARTED TO MANIFEST\n...\n...\n...\nDISEASTER REVEALED: {disaster["name"]}")
                diseasterRevealed = True
            
            # choose random action
            match random.randint(1,6):
                # make a normal action 3x more likely
                case 1:
                    random.choice(players).action()
                case 2:
                    random.choice(players).action()
                case 3:
                    random.choice(players).action()

                #socail interactions
                case 4:
                    random.choice(players).socialise(random.choice(players))
                #diseaster effects
                case 5:
                    random.choice(players).disasterEfect()
                #player murder deaths
                case 6:
                    random.choice(players).kill(random.choice(players))
    
    else:
        # command entered
        # tokenise command
        command = userInput.split(" ")
        match command[0]:
            case "/help":
                # display options
                print(f"/kill {YELLOW}<name>{END}\n\tkills a player")
                print(f"/revive {YELLOW}<name>{END}\n\trevives a player")
                print(f"/create {YELLOW}<name>{END} {YELLOW}<alignment>{END}\n\tadds a new player")
                print(f"/players\n\tlists currently alive players")
                print(f"/update {YELLOW}<name>{END} {YELLOW}<property>{END} {YELLOW}<value>{END}\n\tupdates a property of a player")
            
            case "/kill":
                found = False
                for i in range(len(players)):
                    # if players name matches input
                    if players[i].name == command[1]:
                        # remove from players list
                        print(f"\t{YELLOW}{players[i]}{END} was killed")
                        del[players[i]]
                        found = True
                        break
                        
                if not found:
                    # no players removed
                    print(f"{RED}\tERROR: player does not exist{END}")
            
            case "/revive":
                # add player back to list
                # check if player name exists
                if command[1] in [i.name for i in allPlayers]:
                    # player exists (but may be alive or dead)
                    if command[1] in [i.name for i in players]:
                        # player is already in the game and alive
                        print(f"{RED}\tERROR: player is already alive{END}")
                    else:
                        # player is not alive and exists
                        players.append(Player(command[1], [i["alignment"] for i in data["players"] if i["name"] == command[1]][0]))
                        print(f"\t{YELLOW}{players[-1]}{END} has been revived")
                else:
                    print(f"{RED}\tERROR: player does not exist{END}")
            
            case "/create":
                if command[1] in allPlayers:
                    # player exists
                    print(f"{RED}\tERROR: player already exists{END}")
                else:
                    # attempt to add a new player
                    if command[2] not in ["hider", "explorer", "fighter"]:
                        # alignment is invalid
                        print(f"{RED}\tERROR: invalid alignment{END}")
                    else:
                        #valid name & alignment
                        players.append(Player(command[1], command[2]))
                        print(f"{YELLOW}{players[-1]}{END} has been created")
            
            case "/players":
                for i in players: print(f"\t{i}")
            
            case "/update":
                # check if player exists
                if command[1] not in [i.name for i in allPlayers]:
                    # player doesn't exists
                    print(f"{RED}\tERROR: player does not exist{END}")
                    
                
                else:
                    # player exists
                    # find player index in players and allPlayers
                    for i in range(len(players)):
                        if players[i].name == command[1]:
                            # player found
                            playerIndex = i
                            break
                    
                    for i in range(len(allPlayers)):
                        if allPlayers[i].name == command[1]:
                            # player found
                            allPlayerIndex = i
                            break
                    
                    match command[2]:
                        case "name":
                            if command[3] in [i.name for i in allPlayers]:
                                # name used by someone else
                                print(f"{RED}\tERROR: player name already in use{END}")
                            else:
                                # name unused
                                # update both lists of players
                                players[playerIndex].name = command[3]
                                allPlayers[allPlayerIndex].name = command[3]
                                print(f"\tchanged {YELLOW}{command[1]}'s{END} name to {YELLOW}{command[3]}{END}")
                        case "alignment":
                            if command[3] in ["hider", "explorer", "fighter"]:
                                # user entered valid alignment
                                players[playerIndex].alignment = command[3]
                                allPlayers[allPlayerIndex].alignment = command[3]
                                print(f"\tchanged {YELLOW}{command[1]}'s{END} alignment to {YELLOW}{command[3]}{END}")
                            else:
                                print(f"{RED}\tERROR: unknown alignment{END}")
                                
                        case _:
                            print(f"{RED}\tERROR: unknown property{END}")
            
            case _:
                # entered command is invalid
                print(f"{RED}\tERROR: invalid command, use /help for help{END}")