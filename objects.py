import time
import datetime
import math


# USER OBJECT TO STORE INFORMATION ABOUT USER THROUGHOUT GAME
class User(object):
	def __init__(self):
		self.date = datetime.datetime(1848, 4, 6)
		self.miles_to_go = 2000
		self.health = 100
		self.money = 0
		self.choices = [] # stores user keystrokes -- not being used for anything currently

	# INCREMENT DATE
	def next_day(self):
		self.date = self.date + datetime.timedelta(days=1)

	# USED FOR PRINTING DATE IN GAME SCRIPT.
	# RETURN READABLE VERSION OF DATE
	def date_pretty(self):
		# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
		ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
		return self.date.strftime("%B") + " " + ordinal(self.date.day) + ", " + str(self.date.year)

	# DECREASE MILES BY AMOUNT - UNABLE TO INCREASE MILES IN THIS GAME.
	# RETURN TRUE IF MILES TO GO REACHES ZERO.
	# PARAMETERS:
	#	- amount
	def decrease_miles_to_go(self, amount):
		self.miles_to_go -= amount
		if self.miles_to_go <= 0:
			self.miles_to_go = 0 # miles_to_go cannot be negative
			return True
		else:
			return False

	# INCREASE HEALTH BY AMOUNT.
	# HEALTH CANNOT SURPASS 100.
	# PARAMETERS:
	#	- amount
	def increase_health(self, amount):
		self.health = min(self.health + amount, 100)

	# DECREASE HEALTH BY AMOUNT.
	# RETURN FALSE IF HEALTH REACHES ZERO.
	# PARAMETERS:
	#	- amount
	def decrease_health(self, amount):
		self.health -= amount
		if self.health <= 0:
			return False
		else:
			return True

	# INCREASE MONEY BY AMOUNT.
	# PARAMETERS:
	#	- amount
	def increase_money(self, amount):
		self.money += amount

	# DECREASE MONEY BY AMOUNT.
	# NO SAFEGUARDS AGAINST DECREASING TO NEGATIVE VALUE, THIS IS HANDLED IN BUY_ITEM FUNCTION IN INVENTORY.
	# PARAMETERS:
	#	- amount
	def decrease_money(self, amount):
		self.money -= amount

	# ADD USER CHOICE TO LIST OF USER CHOICES THROUGHOUT GAME
	def add_choice(self, choice):
		self.choices.append(choice)

	def __str__(self):
		return "Miles to go: {}, Money left: {}, Health: {}".format(self.miles_to_go, self.money, self.health)


# ITEMS AVAILABLE FOR INVENTORY.
# INIT PARAMETERS:
#	- name
#	- description
#	- price: cost to acquire one additional unit of item
class Item(object):
	def __init__(self, name, description, price):
		self.name = name
		self.description = description
		self.price = price

	def __str__(self):
		return "{} (${} per): {}".format(self.name, self.price, self.description)


# CONTAINS DICTIONARY OF ITEMS.
# KEY IS ITEM OBJECT,
# VALUES IS QUANITITY OF ITEM HELD IN INVENTORY
class Inventory(object):
	def __init__(self):
		self.items = {}

	# RETURN LIST OF ITEMS IN INVENTORY
	def options(self):
		return list(self.items.keys())

	# ADD QUANTITY AMOUNT OF ITEM TO INVENTORY.
	# IF ITEM ALREADY IN INVENTORY, JUST INCREASE QUANTITY HELD BY SPECIFIED AMOUNT.
	# PARAMETERS:
	#     - item: Item object being added
	#     - quantity: quantity of item to add
	def add_item(self, item, quantity):
		if item not in list(self.items.keys()):
			self.items[item] = quantity
		else:
			self.items[item] += quantity

	# REMOVE QUANTITY OF ITEM IN INVENTORY.
	# RETURN FALSE IF QUANTITY PARAMETER IS GREATER THAN QUANTITY HELD - CANNOT HAVE NEGATIVE QUANTITY.
	# PARAMETERS:
	#     - item: Item object to remove quantity of
	#     - quantity: quantity of item to remove from inventory
	def remove_item(self, item, quantity):
		if item in list(self.items.keys()): # make sure item exists in inventory before trying to remove it
			if quantity <= self.items[item]:
				self.items[item] -= quantity
				return True
			else:
				return False
		else:
			return False

	# BUY ITEM - INCREASE QUANTITY, DECREASE MONEY.
	# RETURN TRUE IF TRANSACTION GOES THROUGH, REQUIRES NON-NEGATIVE MONEY AFTER PROPOSED TRANSACTION.
	# PARAMETERS:
	#     - user:
	#     - item:
	#     - quantity:
	def buy_item(self, user, item, quantity):
		if user.money >= (item.price * quantity):
			self.add_item(item, quantity)
			user.decrease_money(item.price * quantity)
			return True
		else:
			return False

	def __str__(self):
		s = ""
		for item, quantity in self.items.items():
			s += "\n\t- {} {}: {}".format(quantity, item.name, item.description)
		return s

