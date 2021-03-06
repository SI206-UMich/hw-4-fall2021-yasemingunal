
import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount):
        self.wallet -= amount 
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):
        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings
    
    def process_order(self, name, quantity):
        if self.inventory[name] >= quantity:
            self.inventory[name] -= quantity
         
    def has_item(self, foodName, quantity):
        if foodName in self.inventory.keys():
            if self.inventory[foodName] >= quantity:
                return True
        return False
         
    def stock_up(self, foodName, quantity):
        if foodName in self.inventory.keys():
            self.inventory[foodName] += quantity
        else:
            self.inventory[foodName] = quantity 
         
    def compute_cost(self, quantity):
        totalCost = quantity * self.cost
        return totalCost

    def __str__(self):
        return("Hello we are ", self.name, ". This is the current menu ", self.inventory.keys(), ". We charge $", self.cost, " per item. We have $", self.earnings, " in total")


class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        extraTestInventory = {"Ice Cream":10, "Gelato": 12}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.s4 = Stall("Extra for Test!", extraTestInventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        self.c3 = Cashier("Extra", [extraTestInventory])
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements? 
                #There should not be "self.s1"/"self.s3" inside the compute_cost function! 
                #also the costs were calculated incorrectly
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50) #totalcost = 5 * 10 = 50
        self.assertEqual(self.s3.compute_cost(6), 42) #totalcost = 6 * 7 =42
    
	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        # Test to see if has_item returns True when a stall has enough items left
        self.assertEqual(self.s1.has_item("Burger", 3), True)
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertEqual(self.s1.has_item("Burrito", 4), False)
        self.assertEqual(self.s2.has_item("Pita Wrap", 2), False)
        # Test case 2: the stall does not have enough food item: 
        self.assertEqual(self.s1.has_item("Burger", 50), False)
        self.assertEqual(self.s2.has_item("Taco", 86), False)
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertEqual(self.s1.has_item("Taco", 12), True)
        self.assertEqual(self.s3.has_item("Burger", 5), True)

	# Test validate order
    def test_validate_order(self):
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.f1.validate_order(self.c1, self.s1, "Burger", 30) # 30 burgers * $10 = $300
        self.assertEqual(self.f1.wallet, 100) # Tom only has $100 (order will fail, wallet amount will stay same)

        self.f2.validate_order(self.c2, self.s2, "Taco", 30) #30 tacos * $9 = $270 
        self.assertEqual(self.f2.wallet, 150) #Morgan only has $150 (order will fail, wallet amount will stay same)
     
        # case 2: test if the stall doesn't have enough food left in stock
        self.f1.validate_order(self.c1, self.s1, "Burger", 50)
        self.assertEqual(self.s2.inventory["Burger"], 40) #stall only has 40 burgers (order will fail, quantity will not change)

        self.f2.validate_order(self.c2, self.s2, "Taco", 70)
        self.assertEqual(self.s2.inventory["Taco"], 50) #stall only has 50 burgers (order will fail, quantity will not change)

		# case 3: check if the cashier can order item from that stall
        self.f1.validate_order(self.c1, self.s1, "Burger", 10)
        self.assertEqual(self.s1.inventory["Burger"], 30) #this cashier has this stall (order will go through, inventory wil decrease by 10)

        self.f2.validate_order(self.c2, self.s2, "Taco", 2)
        self.assertEqual(self.s2.inventory["Taco"], 48) #this cashier has this stall (order will go through, inventory wil decrease by 2) 
        # case 4: check if vendor doesn't have the stall
        self.f2.validate_order(self.c3, self.s2, "Burger", 4)
        self.assertEqual(self.s2.inventory["Burger"], 30) #this vendor doesn't have this stall (order will fail, inventory won't change from last decrease in line 219)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        #adding 20 to the default value of 100 inside customer f1's wallet (should be $120 in wallet after money is reloaded):
        self.f1.reload_money(20)
        self.assertEqual(self.f1.wallet, 120) 
        #adding 30 to inputted value of 150 inside customer f2's wallet (should be $180 in wallet after money is reloaded):
        self.f2.reload_money(30)
        self.assertEqual(self.f2.wallet, 180)
    
### Write main function
def main():
    #Create different objects 
    mushroom_inventory = {"Maitake": 6, "Portabello": 12, "Oyster": 30}
    veggie_inventory = {"Spinach": 15, "Carrot": 24, "Cabbage": 24}
    fruit_inventory = {"Plum": 16, "Apple": 22, "Orange": 15}

    yaseminCustomer = Customer("Yasemin", 125)
    aylinCustomer = Customer("Aylin", 190)
    mayaCustomer = Customer("Maya", 79)

    mushroomStall = Stall("Mushroom Manshion", mushroom_inventory, 12)
    veggieStall = Stall("Vegetable Station", veggie_inventory, 6)
    fruitStall = Stall("Fruit Station", fruit_inventory, 9)

    mushroomCashier = Cashier("Jane", [mushroomStall])
    produceCashier = Cashier("John", [veggieStall, fruitStall])

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    yaseminCustomer.validate_order(mushroomCashier, veggieStall, "Spinach", 5)
    aylinCustomer.validate_order(mushroomCashier, fruitStall, "Orange", 7)
    mayaCustomer.validate_order(produceCashier, mushroomStall, "Maitake", 12)
    #case 2: the cashier has the stall, but not enough ordered food or the ordered food item
    yaseminCustomer.validate_order(mushroomCashier, mushroomStall, "Maitake", 9)
    aylinCustomer.validate_order(produceCashier, veggieStall, "Cabbage", 30)
    mayaCustomer.validate_order(produceCashier, fruitStall, "Apple", 32)
    #case 3: the customer does not have enough money to pay for the order: 
    yaseminCustomer.validate_order(produceCashier, veggieStall, "Carrot", 20)
    aylinCustomer.validate_order(produceCashier, fruitStall, "Apple", 22)
    mayaCustomer.validate_order(mushroomCashier, mushroomStall, "Portabello", 10)
    #case 4: the customer successfully places an order
    yaseminCustomer.validate_order(mushroomCashier, mushroomStall, "Oyster", 1)
    aylinCustomer.validate_order(produceCashier, veggieStall, "Spinach", 1)
    mayaCustomer.validate_order(produceCashier, fruitStall, "Orange", 2)

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
