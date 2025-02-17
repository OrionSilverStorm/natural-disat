import random
import json

#---------------------------------------------------------------------------------------------------------Read in json
#open json file
data = json.load(open("data.json", "r"))

#choose current map
currentMap = random.choice(data["maps"])
diseasterRevealed = False

#-----------------------------------------------------------------------------------------------------------------FUNCy code
class Player: pass # stops python complaining about type hinting
class Player:
    def __init__(self, name: str, alignment: str) -> None:
        # create a player with a name and alignment
        self.name = name
        self.alignment = alignment
    
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
        # have the calling object kill another player
        if self == other:
            # if it is the same player, do a sucide
            print(f"{self.name} {random.choice(data["suicides"])}")
        else:
            # calling player kills other player
            print(f"{self.name} {random.choice(data["socailDeaths"])} {other.name}")
        
        # remove the other playe from the list of players
        players.remove(other)
    
    def disasterEfect(self) -> None:
        # check if the disaster is revealed
        if diseasterRevealed:
            # kill someone with the disaster specific deaths
            print(f"{self.name} {random.choice(disaster["deaths"])}")
        else:
            # show sign of disaster
            print(f"{self.name} {random.choice(disaster["warnings"])}")

# creates player objects based on json data
players = [Player(i["name"], i["alignment"]) for i in data["players"]] # alive players
allPlayers = players.copy() # all players that have ever existed
#                   ^^^^^^^
# use .copy() because by default it is only copied by reference

# set the disaster
# TODO relative probabilities from json
if random.randint(0, 100)>= 50:# probability of map specific disaster
    match map:
        case "London":
            disaster = [i for i in data["disasters"] if i["name"] == "Great Deppression"]

        #base case
        case _:
            disaster = random.choice(data["disasters"])
else:
    disaster = random.choice(data["disasters"])


# main game loop ==============================================================================================================================
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


print(f"\nSite:{currentMap}\nDisaster Unkown\n")

gameWon = False
while not gameWon:
    userInput = input()

    if userInput == "":
        # if no command is entered, continue the game

        if len(players) == 1:
            # check if there is only one player left
            # if there is print the winner and stop the game
            print(f"THE SOLE SURVIVER OF THE DISEASTER: {disaster["name"]} IN {currentMap}\nWINNER:{players[0].name} the {players[0].alignment}")
            gameWon = True
            
        else:
            #ChooseAction(diseasterRevealed)
            # chech if disaster is revealed and if not maybe reveal it
            if not diseasterRevealed and (random.randint(0,100) > 95 or len(players) < 5):
                #if rng or player list is low
                print(f"DISEASTER HAS STARTED TO MANIFEST\n...\n...\n...\nDISEASTER REVEALED: {disaster["name"]}")
                diseasterRevealed = True
            
            # choose action
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
        # options are /kill, /revive, /help, /createPlayer
        match command[0]:
            case "/help":
                # display options
                print("/kill <name>\n    kills a player")
                print("/revive <name>\n    revives a player")
                print("/create <name> <alignment>\n    adds a new player")
            
            case "/kill":
                found = False
                for i in range(len(players)):
                    # if players name matches input
                    if players[i].name == command[1]:
                        # remove from players list
                        del[players[i]]
                        found = True
                        
                if not found:
                    # no players removed
                    print("ERROR: player not found")
            
            case "/revive":
                # add player back to list
                # check if player name exists
                if command[1] in allPlayers:
                    # player exists (but may be alive or dead)
                    if command[1] in [i.name for i in players]:
                        # player is already in the game and alive
                        print("ERROR: player is already alive")
                    else:
                        # player is not alive and exists
                        players.append(Player(command[1], [i["alignment"] for i in data["players"] if i["name"] == command[1]][0]))
                        print(f"{players[-1].name} has been revived")
                else:
                    print("ERROR: player does not exist, to create a new player use /create")
            
            case "/create":
                if command[1] in allPlayers:
                    # player exists
                    print("ERROR: player already exists")
                else:
                    # attempt to add a new player
                    if command[2] not in ["hider", "explorer", "fighter"]:
                        # alignment is invalid
                        print("ERROR: invalid alignment")
                    else:
                        #valid name & alignment
                        players.append(Player(command[1], command[2]))
            
            case _:
                # enterd command is invalid
                print("invalid command, use /help for help")