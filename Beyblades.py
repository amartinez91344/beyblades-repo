import random
import sys
import math
import time
class Beyblade: 
  # Beyblade class which determines stats, upgrades, and current state.
  def __init__(self, name, attack = 20, defense = 20, health = 100, upgrades = [], isBroken = False):
    self.name = name
    self.attack = attack
    self.defense = defense
    self.upgrades = []
    self.health = health
    self.isBroken = isBroken
    self.attack_buff = 0 
    self.defense_buff = 0 
    for upgrade in self.upgrades:
      self.attack_buff += upgrade.att_up
      self.defense_buff += upgrade.def_up
 
  def __repr__(self):
    #Prints a list of stats, upgrades, and current state.
    if self.upgrades == []:
      upgrades_str = "None"
    else:
      upgrades_str = ""
      for upgrade in self.upgrades:
        upgrades_str += upgrade.name 
    if self.isBroken == True: 
      broken = "BROKEN"
    else:
      broken = "WORKING"
    desc = "---------------\n" + self.name.upper()+"\nStatus: " + str(broken) + "\nHealth: " + str(self.health) +"\nAttack: " + str(self.attack) +" + "+ str(self.attack_buff) + "\nDefense: " + str(self.defense)  +" + "+ str(self.defense_buff) + "\nActive upgrades: "+ upgrades_str
    return desc

  def break_beyblade(self):
    self.isBroken = True
    return self.name + " broke!"

  def repair(self):
    self.isBroken = False
    return self.name + " was repaired!"
  
  def apply_upgrade(self, upgrade):
    self.attack_buff += upgrade.att_up
    self.defense_buff += upgrade.def_up

class Upgrade: 
  #upgrade class - items that improve scores of beyblades that can be purchased and applied to beyblades
  def __init__(self, name, att_up, def_up, price):
    self.name = name
    self.att_up = att_up
    self.def_up = def_up
    self.price = price

  def __repr__(self):
    desc = "---------------\n" + self.name.upper() + "\nAttack Increase: "+ str(self.att_up) + "\nDefense Increase: " + str(self.def_up)
    return desc

class Player:
  #player class. can have money, beyblades, and upgrades.
  def __init__(self, money = 5, beyblades = [], upgrades = []):
    self.money = money
    self.beyblades = beyblades
    self.upgrades = upgrades
  
  def __repr__(self):
    beyblade_names = []
    upgrade_names = []
    for blade in self.beyblades:
      beyblade_names.append(blade.name)
    for item in self.upgrades: 
      upgrade_names.append(item.name)
    if self.beyblades == []:
      blades_str = "None"
    else:
      blades_str = ", ".join(beyblade_names)
    if self.upgrades == []:
      upgrades_str = "None"
    else:
      upgrades_str = ", ".join(upgrade_names)
    desc = "Money: " +str(self.money) + "\nBeyblades: "+blades_str  + "\nUpgrades: " + upgrades_str
    return desc
  
  def purchase_upgrade(self, upgrade):
    if self.money < upgrade.price:
      return "You have insufficient funds."
    else:
      self.money -= upgrade.price
      self.upgrades.append(upgrade)
      return "Purchased "+upgrade.name

  def add_money(self, amount):
    self.money += amount
  
  def add_beyblade(self, beyblade):
    self.beyblades.append(beyblade)
  
  def use_upgrade(self,upgrade,beyblade):
    self.upgrades.remove(upgrade)
    beyblade.apply_upgrade(upgrade)

def menu(player):
  # Main menu 
  print("\n~~~~~~ M E N U ~~~~~~\n1. Inventory\n2. Shop\n3. Let \'em RIIIP\n4. Quit\n")
  choice = input()
  if choice == "1": 
    inventory(player)
  elif choice =="2":
    shop(player,shop_upgrades)
  elif choice == "3":
    battle(player)
  elif choice == "4":
    choice = input("Are you sure you want to quit? Y/N\n")
    if choice == "Y" or choice == "y":
      sys.exit()
    else:
      menu(player)
  else:
    print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
    menu(player)

def inventory(player):
  print("\n")
  for blade in player.beyblades:
    print(blade)
  for item in player.upgrades:
    print(item)

  try:
    choice = int(input("\n1. Apply Upgrade\n2. Return to menu\n\n"))
  except ValueError: 
    print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
    inventory(player)
  if choice == 1:
    if player.upgrades == []:
      print("You don't have any upgrades! You can purchase them from the shop.")
      inventory(player)
    else:
      print("Select your upgrade: ")
      count = 1
      for item in player.upgrades:
        print(str(count)+". "+item.name)
        count +=1
      try:
        upgrade_choice = int(input())
      except ValueError:
        print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
        inventory(player)
      if upgrade_choice >= count:
        print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
        inventory(player)
      print("\nSelect your beyblade:")
      count = 1
      for blade in player.beyblades:
        print(str(count)+". "+blade.name)
        count +=1
      try:
        blade_choice = int(input())
      except ValueError:
        print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
        inventory(player)
      if blade_choice >= count:
        print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
        inventory(player)
      
      print("blade_choice: "+str(blade_choice))
      print("upgrade_choice: " + str(upgrade_choice))
      player.beyblades[blade_choice-1].upgrades.append(player.upgrades[upgrade_choice-1]) #add upgrade to beyblade upgrade list
      player.beyblades[blade_choice - 1].apply_upgrade(player.upgrades[upgrade_choice - 1 ]) # apply the upgrade to the beyblade of choice
      player.upgrades.pop(upgrade_choice-1) #remove upgrade from player inventory
      print("\n Upgrade Applied.") 
      inventory(player)

  menu(player)
  

def shop(player,upgrades):
  #Shop where players can purchase upgrades
  print("\n~~~~~~ S H O P ~~~~~~\n")
  print("Cash: "+str(player.money))
  print("\n    ITEM             PRICE")
  inventory_count = 0 # to keep track of the shop item list
  for item in upgrades:
    print(str(upgrades.index(item)+1)+". "+item.name+"      "+str(item.price))
    inventory_count+=1
  print(str(inventory_count+1) + ". Repair Beyblade     25") # repair always third to last option
  print(str(inventory_count+2) + ". New Beyblade        50") # new beyblade always second to last option
  print(str(inventory_count+3) + ". Return to menu") # return to menu always last option
  try: 
    choice = int(input()) #try to force input to an int
  except ValueError: #retry if a number is not entered
    print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
    shop(player,upgrades) 
  #if type(choice) 
  if choice <= inventory_count and choice > 0: # purchase an upgrade
    choice -= 1
    if player.money >= upgrades[choice].price:
      print("\n"+upgrades[choice].name.strip() + " added to inventory.")
      player.upgrades.append(upgrades[choice])
      player.money-=upgrades[choice].price
      upgrades.pop(choice)
      shop(player,upgrades)
    else:
      print("\nInsufficient funds.")
      shop(player,upgrades)
  elif choice == inventory_count+2: # purchase a new beyblade. 
    if player.money <50:
      print("\nInsufficient funds.")
    else:
      player.money-= 50
      name = input("Name your new beyblade.\n")
      player.beyblades.append(Beyblade(name))
      print(name+" was added to your inventory.")
      shop(player,upgrades)
  elif choice == inventory_count+1: # repair beyblade. as written repairs all beyblades.
    if player.money >= 5:
      for blade in player.beyblades:
        if blade.health >= 81:
          blade.health = 100
        else:
          blade.health += 20
      print("Beyblade(s) repaired.")
      player.money -= 25 
      shop(player,upgrades)
    else:
      print("\nInsufficient funds.")
      shop(player,upgrades)
  elif choice == inventory_count + 3:
    menu(player)
  else:
    print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
    shop(player,upgrades)

def battle(player):
  #TODO choose beyblade, battle (in stages maybe?) based on randomly generated beyblade
  # + win a randomly generated amount of money
  print("\n~~~~~ B A T T L E ~~~~~\nChoose your beyblade:\n")
  count = 1
  for blade in player.beyblades:
    print(str(count)+". "+blade.name.upper()+"\n")
    count+=1
  try:
    choice = int(input())
  except: 
    print("Command not recognized. Type in the number corresponding to your choice and hit enter.")
    battle(player) 
  p1_blade = player.beyblades[choice-1]
  # generate an opponent's beyblade based on selected beyblade's base stats (so upgrades actually give an advantage)
  # +/- 20% on opponent stats
  p2_att = random.randint(math.floor(p1_blade.attack), math.ceil(p1_blade.attack*1.5))
  p2_def = random.randint(math.floor(p1_blade.defense), math.ceil(p1_blade.defense*1.5))
  p2_hel = random.randint(math.floor(p1_blade.health*0.8),100)
  p2_blade = Beyblade("P2",p2_att,p2_def,p2_hel)
  p1_att = p1_blade.attack
  p1_def = p1_blade.defense
  p1_hel = p1_blade.health
  for upgrade in p1_blade.upgrades:
    p1_att += upgrade.att_up
    p1_def += upgrade.def_up
  #battles go as follows: beyblades clash 3 to 5 times, upon each clash health is removed equal to the attacker's attack stat minus the defender's defense stat. after clashes are done, 
  # the blade that did the most damage wins. loser pays the winner $5. 
  clash_count = random.randint(3,5)
  if p1_def > p2_att:
    p1_damage = 0
  elif p1_def <= p2_att:
    p1_damage = p2_att - p1_def
  if p2_def > p1_att:
    p2_damage = 0
  elif p2_def <= p1_att:
    p2_damage = p1_att - p2_def
  print("Ready.....")
  time.sleep(1)
  print("3!")
  time.sleep(0.5)
  print("2!")
  time.sleep(0.5)
  print("1!")
  time.sleep(0.5)
  print("LET EM RIIIP!")

  for i in range(clash_count+1):
    if i < clash_count:
      print("\n          "+p1_blade.name.upper()+"        OPPONENT")
      print("Attack:   "+str(p1_att)+"        "+str(p2_att))
      print("Defense:  "+str(p1_def)+"        "+str(p2_def))
      print("Health:   "+str(p1_hel)+"       "+str(p2_hel))
      p1_hel -= p1_damage
      p2_hel -= p2_damage
      time.sleep(2)
      print("\n\n\n\n\n\n\n\n\n\n        CRASH!!\n\n")
    elif i == clash_count:
     print("\n          "+p1_blade.name.upper()+"        OPPONENT")
     print("Attack:   "+str(p1_att)+"        "+str(p2_att))
     print("Defense:  "+str(p1_def)+"        "+str(p2_def))
     print("Health:   "+str(p1_hel)+"       "+str(p2_hel))
     p1_hel -= p1_damage
     p2_hel -= p2_damage
     time.sleep(1)
    elif i == 1:
      print("\n          "+p1_blade.name.upper()+"        OPPONENT")
      print("Attack:   "+str(p1_att)+"        "+str(p2_att))
      print("Defense:  "+str(p1_def)+"        "+str(p2_def))
      print("Health:   "+str(p1_hel)+"       "+str(p2_hel))
      p1_hel -= p1_damage
      p2_hel -= p2_damage
      time.sleep(4)
      print("\n\n\n\n\n\n\n\n\n\n        CRASH!!\n\n")
    if p1_hel <= 0 or p2_hel <= 0: # exit battle if either beyblade reaches 0 health
      break 

  if p1_damage > p2_damage: #p2 did more damage, p2 wins
    print("\nYou lose! You paid your opponent $5.\n")
    player.money -= 5
  elif p1_damage < p2_damage: #p1 did more damage, you win
    print("\nYou win! Your opponent paid you $5.\n")
    player.money += 5
  elif p1_damage == p2_damage:
    print("\nIt was a tie!\n")
  player.beyblades[choice-1].health-=p1_damage
  menu(player)


shop_upgrades = [Upgrade("Toothpicks    ", 20, 0, 2), Upgrade("Tinfoil       ", 0, 20, 20), Upgrade("Plastic Knives", 50, 0, 100), Upgrade("Silly Putty   ", 0, 50, 100), Upgrade("Metal Spikes  ", 100,0,500), Upgrade("Electromagnet ",0,100,500)]
p1 = Player()
print("Welcome to the wonderful world of beyblades. ")
name = input("Give your first beyblade a name by typing it in and pressing enter.\n")
p1.add_beyblade(Beyblade(name))
print("\n"+name + " has been added to your inventory.\n")
menu(p1)