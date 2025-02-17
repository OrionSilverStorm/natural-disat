import random
import json

#---------------------------------------------------------------------------------------------------------Read in json
#open json file
data = json.load(open("data.json", "r"))
###players = [Player(i, "hider") for i in data["hiderList"]] + [Player(i, "explorer") for i in data["explorerList"]] + [Player(i, "fighter") for i in data["fighterList"]]

# init vars
totalPlayerList = []
contInput = True
contValidation = True
contMain = True
#choose current map
currentMap = random.choice(data["maps"])
diseasterRevealed = False

#-----------------------------------------------------------------------------------------------------------------FUNC

class Player:
    def __init__(self, name, alignment):
        # create a player with a name and alignment
        self.name = name
        self.alignment = alignment
    
    def action(self):
        # make a single player (the calling object) do an action
        print(f"{self.name} {random.choice(data[self.alignment + "Actions"])}")
        #                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
        # this gets the players alignment and appends "Actions" to it to get the list of actions for that alignment
        # then it chooses a random action from that list
    
    def socialise(self, other):
        # make a player (the calling object) socialise with another player (the "other" object)
        if self == other:
            # if it is the same player, do a hallucination
            print(f"{self.name} {random.choice(data["hallucinations"])}")
        else:
            # otherwise, do a normal social interaction
            print(f"{self.name} {random.choice(data["socailInteractions"])} {other.name}")
    
    def kill(self, other):
        # have the calling object kill another player
        if self == other:
            # if it is the same player, do a sucide
            print(f"{self.name} {random.choice(data["suicides"])}")
        else:
            # calling player kills other player
            print(f"{self.name} {random.choice(data["socailDeaths"])} {other.name}")
        
        # remove the other playe from the list of players
        players.remove(other)
    
    def disasterEfect(self):
        # check if the disaster is revealed
        if diseasterRevealed:
            # kill someone with the disaster specific deaths
            print(f"{self.name} {random.choice(disaster["deaths"])}")
        else:
            # show sign of disaster
            print(f"{self.name} {random.choice(disaster["warnings"])}")

players = [Player(i["name"], i["alignment"]) for i in data["players"]]

def choseDisaster(map: str) -> dict:
    if random.randint(0, 100)>= 50:# probability of map specific disaster
        match map:
            case "London":
                disaster = [i for i in data["disasters"] if i["name"] == "Great Deppression"]

            #base case
            case _:
                disaster = random.choice(data["disasters"])
    else:
        disaster = random.choice(data["disasters"])
    
    return disaster

                

# choose map, if specail map choose speacil diseaster
# then get the disaster


disaster = choseDisaster(currentMap)

#player actions for each alignement

#-----------------------------
print("WELCOME TO YOUR DOOM - NATURAL DISASTER SIMULATOR\nEnter the players:\n ")
playerInput = ""
while contInput:
    playerInput = str(input("Enter new Player name(Enter to skip entering extra people): "))

    if playerInput == "":
        contInput = False
        contValidation = False

    #input validation
    while contValidation:
        try:
            pAlignment = int(input("\nWhat is you goal? (1 to hide, 2 to explore, 3 to rampage): "))
        except ValueError:
            print("Please be aware of the existence of numbers and/or proper literacy, kindly retry")
        else:
            if int(pAlignment) < 1 or int(pAlignment) > 3:
                print("Wrong range of values")
            else:
                contValidation = False

    if playerInput != "":
        match pAlignment:
            case 1:
                data["hiderList"].append(playerInput)
            case 2:
                data["explorerList"].append(playerInput)
            case 3:
                data["fighterList"].append(playerInput)

# init total player list
#totalPlayerList = data["hiderList"] + data["fighterList"] + data["explorerList"]

print(f"\nSite:{currentMap}\nDisaster Unkown\n")

gameWon = False
while not gameWon:
    usrInput = input()

    if usrInput == "":

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
        command = usrInput.split(" ")
        if command[0] == "/Revive":
                totalPlayerList.append(command[2])     
                if command[1] == "hider":
                        data["hiderList"].append(command[2])

                if command[1] == "fighter":
                        data["fighterList"].append(command[2])
                        
                if command[1] == "explorer":
                        data["hiderList"].append(command[2])
                print(f"{command[3]} has been revivied")

        elif command[0] == "/kill":
                totalPlayerList.remove(command[2])     
                if command[1] == "hider":
                        data["hiderList"].remove(command[2])

                if command[1] == "fighter":
                        data["fighterList"].remove(command[2])
                        
                if command[1] == "explorer":
                        data["hiderList"].remove(command[2])
                print(f"{command[3]} has been killed")
