stock = {
    'Bread': {'price': 65, 'quantity': 20}, 
    'Milk': {'price': 95, 'quantity': 19}
         }

# for product, details in stock.items():
#     price = details['price']
#     quantity = details['quantity']
"""
4. Selling a Product
Ask which product and how many units. Check there's enough stock using a conditional - if not, print a clear message and don't sell anything.
If there IS enough stock, reduce the quantity, calculate the total price, and record the sale.
Each sale should be stored as a TUPLE (or similar) in a sales log LIST, e.g. (item, quantity, total, ...).
Keep a SET of every unique product name sold today - update it every time a sale happens.
"""
products_sold = set()
sale_log = []
def sell_product(stock, sale_log, products_sold):

    print("Sell a Product")

    while True:

        product = input("Enter the name of the product(or 0 to exit): ").strip().title()

        if product == "0":
            print("Exiting sales...")
            break

        if product.isdigit():
            print("Enter a valid product name")
            continue

        if product not in stock:
            print("The product is not available")
            continue

        while True:
            quantity = input("Enter number of units(or 0 to exit): ")

            if quantity == "0":
                    print("Exiting sales...")
                    break

            if not quantity.isdigit():
                print("Enter valid units")
                continue

            quantity = int(quantity)

            if quantity <= 0:
                print("Quantity must be greater than 0")
                continue

            if quantity > int(stock[product]['quantity']):
                print(f"Not enough stock available. Only {stock[product]['quantity']} units remaining")
                continue

        
            total_price = stock[product]["price"] * quantity

            stock[product]["quantity"] -= quantity
                
            sale = (product, quantity, total_price)
            sale_log.append(sale)

            # Add product to set
            products_sold.add(product)

            print("\nSALE RECORDED")
            print(f"Product: {product}")
            print(f"Price: Kes {stock[product]['price']}")
            print(f"Quantity Sold: {quantity}")
            print(f"Total Price: Kes {total_price}")
            print()
            print(f"\nProducts sold today : {products_sold}")
            print()
            print(f"For Product: {product} | "
            f"Price: Kes {stock[product]['price']} | "
            f"Available Quantity: {stock[product]['quantity']}")
            print()
            break

"""
5. Sales Report

Loop through the sales log and print every sale, nicely formatted.
Calculate and print the TOTAL revenue for the session using an accumulator.
Print how many UNIQUE products were sold today, using your set from Feature 4.
Identify and print the best-selling product (by quantity or revenue - your group's choice, just be consistent).

"""

def view_sales_report(sale_log, products_sold):

    total_revenue = 0

    quantity_sales = {}

    for sale in sale_log:
        product, quantity, total_price = sale


        print()
        print(f"Products Sold".center(10))
        print()
        print(f"Product: {product}")
        print(f"Quantity : {quantity}")
        print(f"Total Price : {total_price}")
        print()

        total_revenue += total_price

        # Track quantity sold for each product
        if product in quantity_sales:
            quantity_sales[product] += quantity
        else:
            quantity_sales[product] = quantity


    print(f"Total generated revenue : {total_revenue}")
    print(f"\n Unique Products sold {products_sold}")
    print()
    print(f"\n Total unique products sold {len(products_sold)}")
    print()

        # Best-selling product
    if quantity_sales:
        best_selling_product = max(
        quantity_sales,
        key=quantity_sales.get)

        print(
        f"BEST-SELLING PRODUCT: {best_selling_product} "
        f"({quantity_sales[best_selling_product]} units)"
        )
    else:
        print("BEST-SELLING PRODUCT: No sales yet")
"""
6. Search Products

Let the user type part of a product name (not necessarily the whole thing) and find matching items in the inventory.
Use string methods to make the search forgiving: .lower() on both the search term and the product names, 
and the in operator to check for a partial match.
Print every matching product with its price and quantity, or a clear 'No matches found' message.

"""

def search_products(stock):

    while True:
        search = input("Search product name(0 to exit): ").strip().lower()

        if search == "0":
            break 

        if search.isdigit():
            print("Invalid search, search by product name")
            continue

        found = False

        for product, details in stock.items():

            if search in product.lower(): # in — allows partial matching

                price = details['price']
                quantity = details['quantity']
            
                print(f"Product: {product:<15} Price: Ksh {price:<6} Quantity: {quantity}")

                found = True

        if not found:
            print("No matches found")

"""
7. Saving and Loading Data (files)

When the program starts, check if a save file exists. If it does, LOAD the inventory from it instead of starting empty. 
If not, start with a small default inventory.
When the user exits (option 6), WRITE the current inventory to a file so it's still there next time the program runs.
Also save the sales log from this session to a separate file (e.g. append each session's sales, don't overwrite history).
You may use plain .txt files with your own comma-separated format from Session 6 - the csv module is NOT required for this project (that comes in Session 7).


"""

# step 1 - check if save file exists
import os

if os.path.exists("kiosk_inventory.txt"):
    print("Save file found")
else:
    print("No save file found")

# step 2 - save the inventory
def save_inventory(stock):
    with open("kiosk_inventory.txt", "w") as f: # "w" - Write - Opens a file for writing, creates the file if it does not exist
        for product, details in stock.items():
            f.write(f"{product},{details['price']},{details['quantity']}\n")

# Load inventory

def load_inventory():
    stock = {}

    with open("kiosk_inventory.txt", "r") as f: # "r" - Read - Default value. Opens a file for reading, error if the file does not exist
        for line in f:
            product, price, quantity = line.strip().split(",")

            stock[product] = {
                "price" : int(price),
                "quantity" : int(quantity)
            }
    return stock
# Step 3 - Save sales history

def save_sales(sale_log):

    with open("kiosk_sales.txt", "a") as f:

        for sale in sale_log:
            product, quantity, total_price = sale
            f.write(f"{product}, {quantity}, {total_price}\n")


# step 4 - Decide what to load when the progam starts
if os.path.exists("kiosk_inventory.txt"):
    stock = load_inventory()
    print("Inventory loaded from save file.")
else:
    stock = {
        "Bread": {"price": 65, "quantity": 20},
        "Milk": {"price": 95, "quantity": 19}
    }
    print("Starting with default inventory.")

"""3. Inventory Management (dictionary)

Store stock as a dictionary: {'Bread': {'price': 65, 'quantity': 20}, ...} - or a similar structure your group agrees on.
Support viewing the full inventory, formatted neatly (aligned columns using the f-string padding skills from Session 6).
Support restocking an existing item OR adding a brand new one if it doesn't exist yet.
Every inventory-changing action should be its own FUNCTION, not inline code in the menu loop.

"""

def restock(stock):
    print("__________________________________________")
    print("INVENTORY MANAGEMENT")
    print("RE - STOCK")

    while True:
        product = input("Enter the name of the product: ").title().strip()
        
        if product.isdigit():
            print("Please Enter a valid name")
            continue
        
        if product not in stock:
            print("Product does not exist, kindly Add the Product in Stock")
            return

        while True:
            add_quantity = input("Enter the quantity of the product: ")
            
            if not add_quantity.isdigit():
                print("Enter valid Quantity in numbers")
                continue
            else:
                add_quantity = int(add_quantity)
                break

        
        stock[product]['quantity'] += add_quantity
        break

    print(f"For Product {product} : Price Kes {stock[product]['price']} : quantity {stock[product]['quantity']}")



     
def add_stock(stock):
    print("__________________________________________")
    print("INVENTORY MANAGEMENT")
    print("ADD STOCK")

    while True:
        product = input("Enter the name of the product: ").strip().title()

        if product.isdigit():
            print("Please Enter a valid name")
            continue

        if product in stock:
            print("Item Already Exists Kindly Restock")
            return
            #break
        
        
        while True:
            price = input("Enter the price of the product: ")

            if not price.isdigit():
                print("Enter valid Price in numbers")
                continue
            else:
                price = int(price)
                break
        while True:


            quantity = input("Enter the quantity of the product: ")

            if not quantity.isdigit():
                print("Enter valid Quantity in numbers")
                continue
            else:
                quantity = int(quantity)
                break
        
        
        stock[product] = {
        'price' : price,
        'quantity' :quantity
        }
        break

    print(f"{product} has been added") 
    print(f"Price: Kes {price}") 
    print(f"Available stock: {quantity}")

def show_stock(stock):
    print("__________________________________________")
    print("INVENTORY MANAGEMENT")
    print("SHOW STOCK")
    print("__________________________________________")

    print(f"{'Product':<15}{'Price (Kes)':<15}{'Quantity':<10}")
    print("-" * 40)

    for product, details in stock.items():
        price = details['price']
        quantity = details['quantity']

        print(f"{product:<15} {price:<15} {quantity:<10}")

"""
1. Welcome & Setup
# On startup, ask for the kiosk's name and the owner's name.
# Print a clean, formatted welcome banner using an f-string, e.g. 'Welcome to Navas's Kiosk Manager, run by Navas Herbert'.
# Clean any name input with .strip() and .title() before using it - don't trust raw input().

# """

kiosk_name = input("Enter Kiosks name: ").strip().title()
owner_name = input("Enter the Owner name: ").strip().title()

print(f"'Welcome to {kiosk_name}, run by {owner_name}'")

"""
2. Main Menu Loop

# Use a while True loop to show a menu and keep running until the user chooses to exit.
# Suggested options: 1) View Stock, 2) Add/Restock a Product, 3) Sell a Product, 4) View Sales Report, 5) Search Products, 6) Exit.
# Validate the menu choice using .isdigit() before converting with int() - don't let a typo crash the whole program.
# If the choice is invalid or out of range, print a friendly message and show the menu again, don't crash.
"""

while True:
    print("_______________________________________")
    print("Menu")
    print("_________________________________________")
    print("1. View Stock")
    print("2. Add/Restock a Product" )
    print("3. Sell a Product")
    print("4. View Sales Report")
    print("5. Search Products")
    print("6. Exit")


    menu_choice = input("Choose Menu(1-6): ")

    if not menu_choice.isdigit():
        print("Choose a valid number option!")
        continue

    menu_choice= int(menu_choice)

    if menu_choice < 1 or menu_choice > 6:
        print("Choice out of range, enter valid choice")
        continue

    if menu_choice == 1:
        show_stock(stock)
    elif menu_choice == 2:
        print("Add/Restock Product")
        print("1. Add stock")
        print("2. Restock")
        print("3. Exit")

        while True:
            option =input("Choose Option(1-3): ")

            if not option.isdigit():
                print("Enter a valid option(1-3): ")
                continue

            option = int(option)

            if option == 1:
                add_stock(stock)
            elif option == 2:
                restock(stock)
            elif option == 3:
                break
            else:
                print("invalid Option")
    elif menu_choice == 3:
        sell_product(stock, sale_log, products_sold)
    elif menu_choice == 4:
        view_sales_report(sale_log, products_sold)
    elif menu_choice == 5:
        search_products(stock)
    elif menu_choice == 6:
        # Save inventory before exiting
        save_inventory(stock)

        # Save this session's sales
        save_sales(sale_log)

        print("Inventory saved successfully.")
        print("Sales history saved successfully.")
        print("Goodbye!")

        break





        
            










  





