import random
import json

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
        # other is always killed, even if self = other
        players.remove(other)
    
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
map = random.choice(list(data["maps"].items()))# TODO json change
# turn the map back into a dictionary
map = {"name": map[0], "RelativeDisasterProbabilities": map[1]}


# set the disaster
# TODO relative probabilities from json
disaster = random.choice(data["disasters"])


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


print(f"\nSite:{map["name"]}\nDisaster Unkown\n")

gameWon = False
while not gameWon:
    userInput = input()

    if userInput == "":
        # if no command is entered, continue the game

        if len(players) == 1:
            # check if there is only one player left
            # if there is print the winner and stop the game
            print(f"THE SOLE SURVIVER OF THE DISEASTER: {disaster["name"]} IN {map["name"]}\nWINNER:{players[0].name} the {players[0].alignment}")
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
        # options are /kill, /revive, /help, /create
        match command[0]:
            case "/help":
                # display options
                print("/kill <name>\n\tkills a player")
                print("/revive <name>\n\trevives a player")
                print("/create <name> <alignment>\n\tadds a new player")
                print("/players\n\tlists currently alive players")
            
            case "/kill":
                found = False
                for i in range(len(players)):
                    # if players name matches input
                    if players[i].name == command[1]:
                        # remove from players list
                        del[players[i]]
                        found = True
                        break
                        
                if found:
                    print(f"\t{command[1]} was killed")
                else:
                    # no players removed
                    print("\tERROR: player not found")
            
            case "/revive":
                # add player back to list
                # check if player name exists
                if command[1] in allPlayers:
                    # player exists (but may be alive or dead)
                    if command[1] in [i.name for i in players]:
                        # player is already in the game and alive
                        print("\tERROR: player is already alive")
                    else:
                        # player is not alive and exists
                        players.append(Player(command[1], [i["alignment"] for i in data["players"] if i["name"] == command[1]][0]))
                        print(f"\t{players[-1].name} the {players[-1].alignment} has been revived")
                else:
                    print("\tERROR: player does not exist, to create a new player use /create")
            
            case "/create":
                if command[1] in allPlayers:
                    # player exists
                    print("\tERROR: player already exists")
                else:
                    # attempt to add a new player
                    if command[2] not in ["hider", "explorer", "fighter"]:
                        # alignment is invalid
                        print("\tERROR: invalid alignment")
                    else:
                        #valid name & alignment
                        players.append(Player(command[1], command[2]))
                        print(f"{players[-1].name} the {players[-1].alignment} has been created")
            
            case "/players":
                for i in players: print(f"\t{i.name} the {i.alignment}")
            
            case _:
                # enterd command is invalid
                print("\tinvalid command, use /help for help")