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
        self.name = name
        self.alignment = alignment
    
    def action(self):
        print(f"{self.name} {random.choice(data[self.alignment + "Actions"])}")
    
    def socialise(self, other):
        if self == other:
            print(f"{self.name} {random.choice(data["hallucinations"])}")
        else:
            print(f"{self.name} {random.choice(data["socailInteractions"])} {other.name}")
    
    def kill(self, other):
        # have the caller kill another person
        if self == other: # self death
            print(f"{self.name} {random.choice(data["suicides"])}")
        else: # player kills other player
            print(f"{self.name} {random.choice(data["socailDeaths"])} {other.name}")
    
    def disasterEfect(self):
        if diseasterRevealed:
            # kill someone with the disaster specific deaths
            print(f"{self.name} {random.choice(disaster["deaths"])}")
        else:
            # show sign of disaster
            print(f"{random.choice(totalPlayerList)} {random.choice(disaster["warnings"])}")


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

def PlayerAction(alignment):# updataed to take just one argument (the alignment) and use that to find players / actions
    #choose p1
    player = random.choice(data[alignment + "List"])

    if len(data[alignment + "List"]) != 0:        
        #pick a player and their respective alignment action
        print(f"{player} {random.choice(data[alignment + "Actions"])}")

def PlayerSocailInteractions():
    player1 = random.choice(totalPlayerList)
    player2 = random.choice(totalPlayerList)

    #socail intercaction
    print(f"{player1} {random.choice(data["socailInteractions"])} {player2}")

    #check for player dups
    if player1 == player2:
        print(player1 + " " + random.choice(data["hallucinations"]))

#death
def Death(deathType, victim, deathMessage, killer):    
    if deathType == "socail":
        print(f"{victim} {deathMessage} {killer}")

    elif deathType == "enviromental":
        print(f"{victim} {deathMessage}")

    #check for self oppsies
    if victim == killer:
        print(victim + " " + random.choice(data["suicides"]))

    #search to find which faction list the victim is in and removes him
    if victim in data["hiderList"]:
            data["hiderList"].remove(victim)

    elif victim in data["fighterList"]:
            data["fighterList"].remove(victim)

    elif victim in data["explorerList"]:
            data["explorerList"].remove(victim)

    else:
        print("FACTION NOT FOUND")    

    #remove from overall list
    totalPlayerList.remove(victim)

def AnnounceDiseaster():
        global diseasterRevealed
        diseasterRevealed = False
        rng = random.randint(0,100)
        #if rng or player list is low
        if (rng > 100-5 or len(totalPlayerList) < 5) and (not diseasterRevealed):
                print(f"DISEASTER HAS STARTED TO MANIFEST\n...\n...\n...\nDISEASTER REVEALED: {disaster["name"]}")
                diseasterRevealed = True
                
#Choose random action
def ChooseAction(diseasterRevealed):

    if not diseasterRevealed:
         AnnounceDiseaster()

    list1 = [1,2,3,4,5,6]
    action = random.choice(list1)
    match action:
        #if list not 0 do the chosen action
        #hide player actions
        case 1:
            if len(data["hiderList"]) != 0: PlayerAction("hider")
        #explore player
        case 2:
            if len(data["explorerList"]) != 0: PlayerAction("explorer")
        #rampagers
        case 3:
            if len(data["fighterList"]) != 0: PlayerAction("fighter")

        #socail interactions
        case 4:
            if len(totalPlayerList) != 0: PlayerSocailInteractions()

        #diseaster deaths
        case 5:
            if diseasterRevealed:
                # kill player
                if len(totalPlayerList) != 0: Death("enviromental", random.choice(totalPlayerList), random.choice(disaster["deaths"]), None)
            else:
                # show signes of disaster
                print(f"{random.choice(totalPlayerList)} {random.choice(disaster["warnings"])}")
            

        #player murder deaths
        case 6:
            if len(totalPlayerList) != 0: Death("socail", random.choice(totalPlayerList), random.choice(data["socailDeaths"]), random.choice(totalPlayerList))

# choose map, if specail map choose speacil diseaster
# then get the disaster


disaster = choseDisaster(currentMap)

#player actions for each alignement

#-----------------------------
print("WELCOME TO YOUR DOOM - NATURAL DISASTER SIMULATOR\nEnter the players:\n ")
playerInput = ""
while contInput:
    playerInput = str(input("Enter new Player name(Enter to quit): "))

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

#init total player list
totalPlayerList = data["hiderList"] + data["fighterList"] + data["explorerList"]

print(f"\nSite:{currentMap}\nDisaster Unkown\n")

while contMain:
    ifEnter = input()

    if ifEnter == "":

        if len(totalPlayerList) == 1:
            winnerFactionOrigin = ""
            winner = totalPlayerList[0]

                #search to find which faction list the victim is in and removes him
            if winner in data["hiderList"]:
                    winnerFactionOrigin = "the hider"

            elif winner in data["fighterList"]:
                    winnerFactionOrigin = "the fighter"

            elif winner in data["explorerList"]:
                    winnerFactionOrigin = "the explorer"

            print(f"THE SOLE SURVIVER OF THE DISEASTER: {disaster["name"]} IN {currentMap}\nWINNER:{totalPlayerList[0]} {winnerFactionOrigin}")
            contMain = False
        else:
            ChooseAction(diseasterRevealed)
    
    else:
        command = ifEnter.split(" ")
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
