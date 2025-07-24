from menu import Menu
from user import User


class CoffeeMachine:
    def __init__(self):
        self.menu = Menu()
        self.current_user = None

    def run(self):
        print("Welcome to the Smart Coffee Machine ")
        self.authenticate_user()

        while True:
            if self.current_user is None:
                self.authenticate_user()
            elif self.current_user.role == "admin":
                self.admin_menu()
            else:
                self.customer_menu()

    def authenticate_user(self):
        while True:
            print("\n 1. Login")
            print(" 2. Register as Customer")
            choice = input("Select an option (1/2): ")

            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                user = User.login(username, password)
                if user:
                    self.current_user = user
                    print(f" Welcome, {user.username} ({user.role})")
                    break
                else:
                    print(" Invalid credentials.")

            elif choice == "2":
                username = input("Choose a username: ")
                password = input("Choose a password: ")
                user = User.register(username, password)
                if user:
                    self.current_user = user
                    break

            else:
                print(" Invalid choice.")

    def customer_menu(self):
        while True:
            print("\nAvailable drinks:")
            self.menu.show_menu()
            choice = input("Choose a drink or type 'logout': ").lower()
            if choice == "logout":
                print("Logging out...")
                self.current_user = None
                break
            elif self.menu.is_available(choice):
                cost = self.menu.resources['menu'][choice]['cost']
                if self.process_payment(cost):
                    self.menu.make_drink(choice)
            else:
                print("Invalid choice or not enough ingredients.")

    def admin_menu(self):
        while True:
            print(
                "\nAdmin Options: [report | refill | add | adduser | logout]")
            choice = input("Enter command: ").lower()
            if choice == "report":
                print(self.menu.resources)
                print(self.menu.sales)
            elif choice == "refill":
                for item in ['water', 'milk', 'coffee']:
                    amt = int(input(f"Add {item} (ml/g): "))
                    self.menu.resources[item] += amt
                self.menu.save_resources()
            elif choice == "add":
                name = input("New drink name: ").lower()
                water = int(input("Water (ml): "))
                milk = int(input("Milk (ml): "))
                coffee = int(input("Coffee (g): "))
                cost = float(input("Cost (Rs.): "))
                self.menu.resources['menu'][name] = {
                    "water": water,
                    "milk": milk,
                    "coffee": coffee,
                    "cost": cost
                }
                self.menu.save_resources()
            elif choice == "adduser":
                uname = input("New username: ")
                pwd = input("Password: ")
                role = input("Role (customer/admin): ").lower()
                if role not in ['admin', 'customer']:
                    print(" Invalid role.")
                else:
                    User.register(uname, pwd, role)
            elif choice == "logout":
                print("Logging out...")
                self.current_user = None
                break
            else:
                print("Unknown admin command.")

    def process_payment(self, cost):
        print(f"\nThe cost is Rs.{cost}")
        method = input("How would you like to pay? [cash/card]: ").lower()

        if method == "card":
            print("Processing card...")
            print("Payment successful ")
            return True

        elif method == "cash":
            print("Please insert coins.")
            try:
                twenty = int(input("How many Rs.20 notes? "))
                fifty = int(input("How many Rs.50 notes? "))
                hundred = int(input("How many Rs.100 notes? "))
                five_hundred = int(input("How many Rs.500 notes? "))

                total = twenty * 20 + fifty * 50 + hundred * 100 + five_hundred * 500
                print(f"You inserted Rs.{total}")

                if total < cost:
                    print("Sorry, not enough money. Money refunded. ")
                    return False
                elif total > cost:
                    change = total - cost
                    print(f"Here is your change: Rs.{change} ")
                print("Payment successful ")
                return True

            except ValueError:
                print("Invalid input. Please use numbers only.")
                return False

        else:
            print("Invalid payment method.")
            return False
