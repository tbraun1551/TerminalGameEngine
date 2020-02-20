import cursor
import time
import colorama
import random
# import game engine and objects
import engine
import objects


# PREPARE TERMINAL - ALWAYS START GAME WITH CLEAR_SCREEN()
engine.clear_screen(colorama.Back.LIGHTWHITE_EX)
print(colorama.Fore.BLACK) # set text to black
cursor.hide()


# GAMEPLAY SETUP:
# INITIALIZE USER - ALWAYS DO THIS TO BEGIN GAME
user = objects.User()

# INITIALIZE INVENTORY - ADD ALL AQUIRABLE ITEMS WITH QUANTITY 0
inventory = objects.Inventory()
ox_item = objects.Item("Ox", "One ox will pull you twenty miles a day, a second ox will help pull you another sixteen, a third another twelve, etc. A sixth ox will not change your speed.", 50)
inventory.add_item(ox_item, 0)
food_item = objects.Item("Food", "Recommended two units per day", 2)
inventory.add_item(food_item, 0)
med_kit_item = objects.Item("Med Kit", "A med kit can be used to increase health, however in some cases it won't work", 15)
inventory.add_item(med_kit_item, 0)


# USER SELECT DIFFICULTY.
# IF EASY, START USER WITH $500; IF HARD, $300
choice = engine.ask_question("Hello... Welcome to my game...\nWhat difficulty would you like to play?", ["Easy", "Hard"], user, line_delay=0.05)
if choice == 1: 
	user.increase_money(300)
else:
	user.increase_money(150)


# CUSTOM MESSAGE WHEN USER WINS GAME
def won_game():
	engine.show_text("Congratulations, you arrived in San Francisco!\nYou ended with ${} and {} health.".format(user.money, user.health))
	time.sleep(2)
	engine.exit_game()


# VISIT STORE WILL BE USED THROUGHOUT THIS GAME.
# VISIT_STORE() INCLUDES AN ANIMATION OF A STORE,
# AND ALLOWS USER TO BUY ANY ITEM INVENTORY UNTIL THEY CHOOSE TO EXIT.
# PARAMETERS:
#     - user: treat passing user in game script methods as passing self in a class - it tracks game information such as money, health, miles to go
#     - inventory: inventory contains all items available for purchase - for this to work, must add every purchasable item to inventory at beginning of game; likely with quantity zero
def visit_store(user, inventory):
	engine.fade_to_mode(mode="dark")
	engine.asciinate_gif("store.gif", "store", SC=0, GCF=1, white_to_at=False, delay=0.02)
	time.sleep(1)

	def make_choice(user, inventory):
		choice = 0
		options_objects = inventory.options()
		options = [i.name for i in options_objects] + ["None"]
		while choice != len(options):
			choice = engine.ask_question("You have...\n\t- ${}{}\n\nWhat would you like to buy?".format(user.money, str(inventory)), options, user, bg_color=colorama.Back.BLACK, animate=False, center_horiz=False, center_vert=False)
			if choice != len(options): # applies to first use case, otherwise redundant
				item = options_objects[choice-1]
				purchase_options = list(range(1,6)) + ["None"]
				# quantities available for food are different than other items
				if item == food_item:
					purchase_options = list(range(10,60,10)) + ["None"]

				quantity = engine.ask_question("How many {} would you like to buy - they cost ${} each?".format(item.name, item.price), purchase_options, user, bg_color=colorama.Back.BLACK, animate=False, center_horiz=False, center_vert=False)
				if quantity != 6:
					if item == food_item:
						quantity *= 10
					bought = inventory.buy_item(user, item, quantity)
					if bought == False:
						engine.show_text("You only have ${}. You need ${} to buy {} units of {}.".format(user.money, item.price*quantity, quantity, item.name), bg_color=colorama.Back.BLACK, animate=False, center_horiz=False, center_vert=False)
						time.sleep(2)

	q = 2
	while q == 2:
		make_choice(user, inventory)
		q = engine.ask_question("Are you sure you would like to exit the store?", ["Yes", "No"], user, bg_color=colorama.Back.BLACK, animate=False, center_horiz=False, center_vert=False)

	engine.fade_to_mode(mode="light")


# IF USER CHOOSES TO USE MED KIT THERE IS A 75% CHANCE IT WILL WORK,
# AND IF IT DOES WORK IT WILL REVIVE 20% OF LOST HEALTH
def use_med_kit():
	if random.random() < 0.75:
		health_increase = round((100 - user.health) * 0.2)
		engine.show_text("The med kit worked! Your health has increased from {} to {}.".format(user.health, user.health+health_increase))
		user.increase_health(health_increase)
		time.sleep(1)
	else:
		engine.show_text("The med kit didn't work, sorry.")
		time.sleep(1)


# SIMULATE DAY WILL BE USED THROUGHOUT THIS GAME.
# EXPLANATION OF FUNCTIONALITY WITHIN FUNCTION BELOW.
# PARAMETERS:
#     - user: refer to visit_store() documentation
#     - inventory: contains items exhausted throughout game, ex. food item can be consumed in simulate_game()
def simulate_day(user, inventory):
	number_ox = inventory.items[ox_item]
	miles_traveled = min(number_ox * (20 - (2 * (number_ox - 1))), 60)
	san_fran = user.decrease_miles_to_go(miles_traveled) # returns True if user.miles_to_go reaches zero
	if san_fran == True: # game over - user won
		won_game()
	else:
		# only way to decrease health in this game is from lack of food (starvation).
		# if user has >= 2 units of food: consume 2, health remains unchanged;
		# if user has 1 unit of food: consume 1, health decreases by 2;
		# if user has no food: health decreases by 5
		amount_food = inventory.items[food_item]
		if amount_food >= 2:
			inventory.remove_item(food_item, 2)
			health_loss = 0
		elif amount_food == 1:
			inventory.remove_item(food_item, 1)
			health_loss = 2
		else:
			health_loss = 5

		# check if user still has health at the end of the day, if not, they die and game ends
		if user.decrease_health(health_loss) == False:
			engine.show_text("You have run out of food and died.\nYou made it to {}. You were {} miles away from San Francisco.".format(user.date_pretty()), user.miles_to_go)
			time.sleep(5)
			engine.exit_game()

		engine.show_text("{}...\nYou traveled {} miles today. You have {} miles remaining on your journey.\nYour health is {}.".format(user.date_pretty(), miles_traveled, user.miles_to_go, user.health), animate=False)
		time.sleep(3)

		# give user option to use med kit at the end of each day.
		# only bring up prompt if they have at least one med kit
		if inventory.items[med_kit_item] > 0:
			use = engine.ask_question("Would you like to use a med kit?", ["Yes", "No"], user, animate=False, center_horiz=False, center_vert=False)
			if use == 1:
				use_med_kit()

		# increment day
		user.next_day()


# FIRST SCENE
engine.show_text("April 6th, 1848...\nYou are about to set out on the 2,000 mile trail from St. Louis, Missouri to San Francisco, California.\nYou have purchased a carriage, but now you must buy the rest of your supplies at the local store.\nAfter today, the next store on your trail won't be for another 200 miles...")
time.sleep(2)
visit_store(user, inventory)


# SIMULATE TO NEXT SCENE
while user.miles_to_go > 1800: # based on number of ox (speed) store can end up being found in a range of 40 miles - if user ends one day at 1805, we will allow them to cover say 35 miles the next day, we will not stop them at 1800 on the dot. This may be changed
	simulate_day(user, inventory)


# SECOND THROUGH FOURTH "SCENES"
for i in range(3):
	engine.show_text("There appears to be a town nearby.\nAfter today, there's no saying how long it will be until you arrive at another...")
	time.sleep(2)
	visit_store(user, inventory)

	# simulate to next scene
	while user.miles_to_go > 1300 - (500 * i): # stores occur at 1300, 800, 300 miles to go
		simulate_day(user, inventory)


# SIMULATE LAST STRETCH
while user.miles_to_go > 0:
	simulate_day(user, inventory)

