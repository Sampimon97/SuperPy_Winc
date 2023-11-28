# Imports
import argparse
import csv
from datetime import datetime, timedelta
import os
import uuid
import matplotlib.pyplot as plt
from typing import Tuple

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

class SuperPy:
    def __init__(self, bought_file='bought.csv', sold_file='sold.csv', date_file='date.txt'):
        self.bought_file = os.path.join(os.getcwd(), bought_file)
        self.sold_file = os.path.join(os.getcwd(), sold_file)
        self.date_file = os.path.join(os.getcwd(), date_file)

        self.bought = self.load_bought()
        self.sold = self.load_sold()
        self.current_date = self.load_current_date()

        self.revenue = 0.0
        self.profit = 0.0

        self.current_date = self.load_current_date()

    def load_current_date(self):
        try:
            with open(self.date_file, 'r') as file:
                return datetime.strptime(file.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return datetime.now().date()

    def save_current_date(self):
        with open(self.date_file, 'w') as file:
            file.write(self.current_date.strftime("%Y-%m-%d"))

    def advance_time(self, days=1):
        current_datetime = datetime.combine(self.current_date, datetime.min.time())
        new_datetime = current_datetime + timedelta(days=days)
        self.current_date = new_datetime.date()
        self.save_current_date()
        print(f"Time moved forward with {days} days. current date: {self.current_date}")



    def load_bought(self):
        try:
            with open(self.bought_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                bought = [row for row in reader]
            return bought
        except FileNotFoundError:
            return []

    def load_sold(self):
        try:
            with open(self.sold_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                sold = [row for row in reader]
            return sold
        except FileNotFoundError:
            return []

        
    
    def save_bought(self):
        with open(self.bought_file, 'w', newline='') as file:
            fieldnames = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date', 'transaction_id', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.bought)

    def save_sold(self):
        with open(self.sold_file, 'w', newline='') as file:
            fieldnames = ['id', 'bought_id', 'sell_date', 'sell_price', 'transaction_id', 'quantity_sold']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.sold)




   

    def add_bought_product(self, product_id, product_name, buy_price, expiration_date, quantity):
        transaction_id = str(uuid.uuid4())
        new_bought_product = {
            'id': product_id,
            'product_name': product_name,
            'buy_date': self.current_date.strftime("%Y-%m-%d"),
            'buy_price': buy_price,
            'expiration_date': expiration_date,
            'transaction_id': transaction_id,
            'quantity': quantity
        }
        self.bought.append(new_bought_product)
        self.save_bought()
        print(f"Product '{product_name}' bought on {self.current_date.strftime('%Y-%m-%d')} and added to 'bought.csv'.")

    def generate_report(self):
        total_products = len(self.bought)
        total_quantity = sum(int(product.get('quantity', 1)) for product in self.bought)

        print(f"\nInventory Report:")
        print(f"Total Products: {total_products}")
        print(f"Total Quantity: {total_quantity}")

        if total_products > 0:
            print("\nProduct Details:")
            for product in self.bought:
                product_id = product.get('id', 'N/A')
                product_name = product.get('product_name', 'N/A')
                buy_date = product.get('buy_date', 'N/A')
                buy_price = product.get('buy_price', 'N/A')
                expiration_date = product.get('expiration_date', 'N/A')
                quantity = product.get('quantity', 'N/A')

                print(f"ID: {product_id}, Name: {product_name}, "
                      f"Buy Date: {buy_date}, Buy Price: {buy_price}, "
                      f"Expiration Date: {expiration_date}, Quantity: {quantity}")
 
    def display_product_count(self):
        product_count = {}

        for product in self.bought:
            product_name = product['product_name']
            quantity = int(product['quantity']) if 'quantity' in product else 1  
            if product_name in product_count:
                product_count[product_name] += quantity
            else:
                product_count[product_name] = quantity

        print("\nProduct Count:")
        for product_name, count in product_count.items():
            print(f"{product_name}: {count}")

   


    def add_sold_product(self, bought_id, sell_date, sell_price, quantity_sold):
    # Zoek het gekochte product op basis van het ID
        bought_product_index = next((index for index, product in enumerate(self.bought) if product['id'] == bought_id), None)

        if bought_product_index is not None:
            bought_product = self.bought[bought_product_index]

            if 'quantity' in bought_product:
                quantity_bought = int(bought_product['quantity'])

                if quantity_bought >= int(quantity_sold):
                # Maak een nieuw verkocht product aan
                    new_sold_product = {
                        'id': len(self.sold) + 1,
                        'bought_id': bought_id,
                        'sell_date': sell_date,
                        'sell_price': sell_price,
                        'transaction_id': bought_product.get('transaction_id', ''),  
                        'quantity_sold': int(quantity_sold)  
                    }

                # Voeg het nieuwe verkochte product toe aan 'sold.csv'
                    self.sold.append(new_sold_product)
                    self.save_sold()

                # Bereken de omzet en winst
                    self.calculate_revenue()
                    self.calculate_profit()

                # Verminder de hoeveelheid van het gekochte product
                    bought_product['quantity'] = str(quantity_bought - int(quantity_sold))
                    self.save_bought()


                    print(f"{quantity_sold} pieces with ID '{bought_id}' sold, and the quantity decreased in 'bought.csv'.")
                else:
                    print(f"insufficient stock of product with ID '{bought_id}' to sell {quantity_sold} pieces.")
            else:
                print(f"Product with ID '{bought_id}' does not have 'quantity' information.")
        else:
            print(f"Product with ID '{bought_id}' not found in the list of purchased products.")




    def display_sold_info(self):
        if not self.sold:
            print("There are no sols products.")
            return
        
        

        print("\nVerkoopinformatie:")
        for sold_product in self.sold:
            bought_id = sold_product['bought_id']
            sell_date = sold_product['sell_date']
            sell_price = sold_product['sell_price']

            # Zoek het verkochte product in de lijst van gekochte producten
            bought_product = next((product for product in self.bought if product['id'] == bought_id), None)

            if bought_product:
                product_name = bought_product['product_name']
                expiration_date = bought_product['expiration_date']

                # Controleer of het product is verlopen
                if expiration_date and sell_date > expiration_date:
                    status = "expired"
                else:
                    status = "not expired"

                print(f"Productnaam: {product_name}, "
                      f"Verkoopdatum: {sell_date}, "
                      f"Verkoopprijs: {sell_price}, "
                      f"Status: {status}")

            else:
                print(f"Product with ID '{bought_id}' not found in the list of bought products.")

        self.plot_sold_product_count()


    def plot_sold_product_count(self):
        sold_product_count = {}

        for sold_product in self.sold:
            product_name = next((bought_product['product_name'] for bought_product in self.bought if bought_product['id'] == sold_product['bought_id']), 'Onbekend')

            if product_name in sold_product_count:
                sold_product_count[product_name] += int(sold_product['quantity_sold'])
            else:
                sold_product_count[product_name] = int(sold_product['quantity_sold'])

        product_names = list(sold_product_count.keys())
        quantities = list(sold_product_count.values())

        plt.bar(product_names, quantities)
        plt.xlabel('Product Name')
        plt.ylabel('Quantity Sold')
        plt.title('Product Sales Distribution')
        plt.show()


    def display_product(self, product_id):
        for bought_product in self.bought:
            if bought_product['id'] == product_id:
                print("\nProduct Details:")
                print(f"ID: {bought_product['id']}")
                print(f"Product Name: {bought_product['product_name']}")
                print(f"Buy Date: {bought_product['buy_date']}")
                print(f"Buy Price: {bought_product['buy_price']}")
                print(f"Expiration Date: {bought_product['expiration_date']}")
                print(f"Transaction ID: {bought_product['transaction_id']}")
                return

        print(f"Product with ID '{product_id}' not found in 'bought.csv'.")

    def remove_sold_product(self, sold_id):
        for sold_product in self.sold:
            if sold_product['id'] == sold_id:
                self.sold.remove(sold_product)
                self.save_sold()
                print(f"Product with ID '{sold_id}' removed from 'sold.csv'.")
                return
        print(f"Product with ID '{sold_id}' not found in 'sold.csv'.")

    


    def remove_bought_product(self, product_id):
        for bought_product in self.bought:
            if bought_product['id'] == product_id:
                self.bought.remove(bought_product)
                self.save_bought()
                print(f"Product with ID '{product_id}' removed from 'bought.csv'.")
                return
        print(f"Product with ID '{product_id}' not found in 'bought.csv'.")


    def calculate_revenue(self):
        self.revenue = sum(float(sold_product['sell_price']) * float(sold_product['quantity_sold']) for sold_product in self.sold)

    def calculate_profit(self):
        self.profit = 0.0

        for sold_product in self.sold:
            bought_id = sold_product['bought_id']
            quantity_sold = float(sold_product.get('quantity_sold', 1))
            sell_price = float(sold_product['sell_price'])

            bought_product = next((product for product in self.bought if product['id'] == bought_id), None)

            if bought_product:
                buy_price = float(bought_product['buy_price'])
                profit_increment = (sell_price - buy_price) * quantity_sold
                self.profit += profit_increment

                print(f"Bought ID: {bought_id}, Quantity Sold: {quantity_sold}, Sell Price: {sell_price}, Buy Price: {buy_price}, Profit Increment: {profit_increment}")

        print(f"Total Profit: {self.profit}")


    def calculate_revenue_profit_over_period(self, start_date: str, end_date: str) -> Tuple[float, float]:
        revenue = 0.0
        profit = 0.0

        for sold_product in self.sold:
            sell_date = sold_product['sell_date']

            if start_date <= sell_date <= end_date:
                sell_price = float(sold_product['sell_price'])
                quantity_sold = float(sold_product['quantity_sold'])

                revenue += sell_price * quantity_sold

                bought_id = sold_product['bought_id']
                bought_product = next((product for product in self.bought if product['id'] == bought_id), None)

                if bought_product:
                    buy_price = float(bought_product['buy_price'])
                    profit += (sell_price - buy_price) * quantity_sold

        return revenue, profit
    

def main():
    parser = argparse.ArgumentParser(description="SuperPy - Inventory Management")
    parser.add_argument('--plot-graph', action='store_true', help='Plot product quantity distribution graph')
    superpy = SuperPy()
    args = parser.parse_args()

    while True:
        if args.plot_graph:
            superpy.plot_sold_product_count()
        print("\nSuperPy - Inventory Management")
        print("1. Add Product 'bought.csv'")
        print("2. Product sell and add to 'sold.csv'")
        print("3. Generate Report")
        print("4. Display Product Count")
        print("5. Sold information display")
        print("6. Product display")
        print("7. Product remove 'bought-csv'")
        print("8. Product remove 'sold.csv'")
        print("9. Move forward in time")
        print("10. Revenue")
        print("11. profit")
        print("12. Report Revenue and Profit over Period")
        print("13. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10/11/12/13): ")

        args = parser.parse_args()
        if args.plot_graph:
            superpy.plot_sold_product_count()
        elif choice == '1':
            product_id = input("Enter product ID: ")
            product_name = input("Enter productname: ")
            buy_price = input("Enter purchase price: ")
            expiration_date = input("Enter expiration date: ")
            quantity = input("Enter quantity: ")
            superpy.add_bought_product(product_id, product_name, buy_price, expiration_date, quantity)
        elif choice == '2':
            product_id_to_sell = input("Enter the ID of the product to be sold: ")
            sell_date = input("Enter the sale date: ")
            sell_price = input("Enter the selling price: ")
            quantity = input("Enter the quantity: ")
            superpy.add_sold_product(product_id_to_sell, sell_date, sell_price, quantity)
        elif choice == '3':
            superpy.generate_report()
        elif choice == '4':
            superpy.display_product_count()
        elif choice == '5':
            superpy.display_sold_info()
        elif choice == '6':
            product_id_to_display = input("Enter the ID of the product you want to display: ")
            superpy.display_product(product_id_to_display)
        elif choice == '7':
            product_id_to_remove = input("Enter the ID of the product from 'bought.csv' that you want to remove: ")
            superpy.remove_bought_product(product_id_to_remove)
        elif choice == '8':
            sold_id_to_remove = input("Enter the ID of the product from 'sold.csv' that you want to remove: ")
            superpy.remove_sold_product(sold_id_to_remove)
        elif choice == '9':
            days_to_advance = int(input("Enter the number of days to advance time: "))
            superpy.advance_time(days_to_advance)
        elif choice == '10':
            superpy.calculate_revenue()
            print("\nFinancial Information:")
            print(f"Revenue: {superpy.revenue}")
        elif choice == '11':
            superpy.calculate_profit()
            print(f"\nTotal Profit: {superpy.profit}")
        elif choice == '12':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            revenue, profit = superpy.calculate_revenue_profit_over_period(start_date, end_date)
            print(f"\nFinancial Information for the Period {start_date} to {end_date}:")
            print(f"Revenue: {revenue}")
            print(f"Profit: {profit}")
        elif choice == '13':
            print("Exiting SuperPy. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
