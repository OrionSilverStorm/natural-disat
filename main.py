import random as r

#---------------------------------------------------------------------------------------------------------LISTS/VARS
disastersList = [
    "Volcanoe Eruption", "Tsunami", "Earthquake", "Tornado", "Asteroid",
    "Great Deppression", "Super Storm", "Blizzard"
]
maps = [
    "Mount Everest", "London", "Antarctica", "Amazon Rainforest", "Atlantis"
]
#hider
hiderActions = [
    "gets drunk on cactus juice", "falls into a sinkhole, yet comes out without a scratch",
    "digs themself into a ditch", "hides in a bush",
    "tries to use a dinosaur as a meat shield", "yawns",
    "finds a shield to defend themself", "gets bored", "befriends a chicken",
]
#explorer
explorerActions = [
    "finds aN UNDERGROUND crypt", "finds an Indianna Jones costume",
    "fights a balraug at the centre of the map",
    "is making makeshift daddy lillus wings to get to the sun",
    "discovers they are adopted",
    "refuses to stop exploring a duegon after losing a limb", "finds a dragon",
    "becomes a bard", "finds a talking coconut", "almost woke up an ancient evil", "is reading the Lord of the rings", "has found the better ending for solo leveling", "is running away from a boulder that wont stop chasing them", "is recreating ceasers death"
]
#fighter
fighterActions = [
    "FINDS AN AXE", "unseamed a goliath from the knave to the chaps",
    "chops a tree", "has decided to eradicate all plant life",
    "causes a forest fire", "evolves into a karen", "man handles a bird",
    "jumps of a cliff\n\nAND SURVIVES",
    "succumbs to their barbarian instincts and rages",
    "made all the cute animals 'go to sleep'", "uses Lucas as a punching bag", "uses Felix as a punching bag", "Yells 'FOR DEMOCRACY AND FREEDOM' while running head first into a hole", "is fending of the USA after accedently finding oil", "hit the ground with a pickaxe", "launches themseleve via a catapult", "gets hunted by wolves", "is hunting wolves", "becomes a werewolf","is napping", "kills a chicken"
]

socailInteractions = [
    "forms a bromance with", "arrests",
    "gets backhanded down a flight of stairs by", "engages in a boxing match with",
    "plunders the camp of", "kidnaps the dog of",
    "is disscussing the current politcal climate with", "is playing russiann roulette", "gets invitied to raid a duengon by"
]
socailDeaths = ["fell into a pit of spikes dug by", "was stabbed by", "was lit onto fire by", "was roasted by a dragon ridden by", "was obliterated by", "gets 180 full scoped by", "got shot by", "eats the poisoniously bad cooking of"]

hallucinationList = ["is talking to themselves", "is hallucinating", "is murmuring to themselves"]

selfOppsieDeaths = ["has committed sekapoko", "has committed a very unnessecary 'kamikaze'", "has chosen the sweet relief of not exisiting anymore",
                    "dipped a finger into the abyss and fell in", "thought self harm was the way to go"]

naturalDisDeaths = [["suffocates from the smoke in the air"], ["drowns"], ["falls into the cracks of the Earth"], ["gets yeeted into oblivion by the strong winds"],
                    ["gets pummeled by an asteriod"], ["dies of regret due to stock market crash"], ["gets shazamed by lightning"], ["dies of frostbite"]]

diseasterSigns = [["see smoke rising in the distance"], ["sees the water recceding", "notices a lack of animals"], ["feels some shaking", "sees animals freaking out"], ["can see strong winds in the horizon", "sees a lack of birds"],
                    ["sees a flashing light in the sky"], ["sees many frantic people in suits panicking"], ["hears a distant boom"], ["starts to see its snowing"]]

hiderList = ["Eris", "Agnes", "Artem", "Luca", "Burney", "Rhodrigo", "Ussop"]
explorerList =["Shiven", "Jacob", "Joe", "Zach", "Xavi", "the Ki-high-ye-on", "Luffy"]
fighterList = ["Lucas", "Felix", "Jospeh", "Harry", "Libby", "Beth", "Sung Jin-Woo", "Zoro"]
totalPlayerList = []
currentDiseaster = ""
contInput = True
contValidation = True
contMain = True
#choose current map
currentMap = r.choice(maps)
diseasterRevealed = False

#-----------------------------------------------------------------------------------------------------------------FUNC

#random func

def Random(min, max):
  return r.randint(min, max)

#choose map, if specail map choose speacil diseaster
match currentMap:
  case "London":
    #use rng to get prob of getting depression
    rng = Random(0, 100)
    if rng >= 50:
        currentDiseaster = "Great Deppression"
    #else just like base case
    else:
      currentDiseaster = r.choice(disastersList)

  #base case
  case _:
    currentDiseaster = r.choice(disastersList)

#player actions for each alignement
def PlayerAction(alignmentList, alignmentActions):  
  #choose p1
  player = r.choice(alignmentList)

  if len(alignmentList) != 0:    
    #pick a player and their respective alignment action
    print(f"{player} {r.choice(alignmentActions)}")

def PlayerSocailInteractions():
  player1 = r.choice(totalPlayerList)
  player2 = r.choice(totalPlayerList)

  #socail intercaction
  print(f"{player1} {r.choice(socailInteractions)} {player2}")

  #check for player dups
  if player1 == player2:
    print(player1 + " " + r.choice(hallucinationList))

#death
def Death(deathType, victim, deathMessage, killer):  
  if deathType == "socail":
    print(f"{victim} {deathMessage} {killer}")

  elif deathType == "enviromental":
    print(f"{victim} {deathMessage}")

  #check for self oppsies
  if victim == killer:
    print(victim + " " + r.choice(selfOppsieDeaths))

  #search to find which faction list the victim is in and removes him
  if victim in hiderList:
      hiderList.remove(victim)

  elif victim in fighterList:
      fighterList.remove(victim)

  elif victim in explorerList:
      explorerList.remove(victim)

  else:
    print("FACTION NOT FOUND")  

  #remove from overall list
  totalPlayerList.remove(victim)

def AnnounceDiseaster():
    global diseasterRevealed
    diseasterRevealed = False
    rng = Random(0,100)
    #if rng or player list is low
    if (rng > 100-5 or len(totalPlayerList) < 5) and (not diseasterRevealed):
        print(f"DISEASTER HAS STARTED TO MANIFEST\n...\n...\n...\nDISEASTER REVEALED: {currentDiseaster}")
        diseasterRevealed = True
#Choose random action
def ChooseAction(diseasterRevealed):

  if not diseasterRevealed:
     AnnounceDiseaster()

  list1 = [1,2,3,4,5,6]
  action = r.choice(list1)
  match action:
    #if list not 0 do the chosen action
    #hide player actions
    case 1:
      if len(hiderList) != 0: PlayerAction(hiderList, hiderActions)
    #explore player
    case 2:
      if len(explorerList) != 0: PlayerAction(explorerList, explorerActions)
    #rampagers
    case 3:
      if len(fighterList) != 0: PlayerAction(fighterList, fighterActions)

    #socail interactions
    case 4:
      if len(totalPlayerList) != 0: PlayerSocailInteractions()

    #diseaster deaths
    case 5:
      #find index of natural diseaster
      diseasterIndex = disastersList.index(currentDiseaster)

      #show diseaster deaths
      if diseasterRevealed == True:
        if len(totalPlayerList) != 0: Death("enviromental", r.choice(totalPlayerList), r.choice(naturalDisDeaths[diseasterIndex]), None)
      #show diseaster signs
      else:
        print(f"{r.choice(totalPlayerList)} {r.choice(diseasterSigns[diseasterIndex])}")

    #player murder deaths
    case 6:
      if len(totalPlayerList) != 0: Death("socail", r.choice(totalPlayerList), r.choice(socailDeaths), r.choice(totalPlayerList))

#-----------------------------
print("WELCOME TO YOUR DOOM - NATURAL DISASTER SIMULATOR\nEnter the players:\n ")
playerInput = ""
while contInput:
  playerInput = str(input("Enter new Player name(x to quit): "))

  if playerInput == "x":
    print("\nPRESS ENTER TO CONTINUE\n")
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

  if playerInput != "x":
    match pAlignment:
      case 1:
        hiderList.append(playerInput)
      case 2:
        explorerList.append(playerInput)
      case 3:
        fighterList.append(playerInput)

#init total player list
for item in hiderList:
  totalPlayerList.append(item)
for item in fighterList:
  totalPlayerList.append(item)
for item in explorerList:
  totalPlayerList.append(item)

print(f"\nSite:{currentMap}\nDisaster Unkown\n")

while contMain:
  ifEnter = input()

  if ifEnter == "":

    if len(totalPlayerList) == 1:
      winnerFactionOrigin = ""
      winner = totalPlayerList[0]

        #search to find which faction list the victim is in and removes him
      if winner in hiderList:
          winnerFactionOrigin = "the hider"

      elif winner in fighterList:
          winnerFactionOrigin = "the fighter"

      elif winner in explorerList:
          winnerFactionOrigin = "the explorer"

      print(f"THE SOLE SURVIVER OF THE DISEASTER: {currentDiseaster} IN {currentMap}\nWINNER:{totalPlayerList[0]} {winnerFactionOrigin}")
      contMain = False
    else:
      ChooseAction(diseasterRevealed)
  
  else:
    command = ifEnter.split(" ")
    if command[0] == "/Revive":
        totalPlayerList.append(command[2])   
        if command[1] == "hider":
            hiderList.append(command[2])

        if command[1] == "fighter":
            fighterList.append(command[2])
            
        if command[1] == "explorer":
            hiderList.append(command[2])
        print(f"{command[3]} has been revivied")

    elif command[0] == "/kill":
        totalPlayerList.remove(command[2])   
        if command[1] == "hider":
            hiderList.remove(command[2])

        if command[1] == "fighter":
            fighterList.remove(command[2])
            
        if command[1] == "explorer":
            hiderList.remove(command[2])
        print(f"{command[3]} has been killed")
