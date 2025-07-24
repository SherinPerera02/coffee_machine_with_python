import json


class Menu:
    def __init__(self):
        with open('data/resources.json') as f:
            self.resources = json.load(f)
        with open('data/sales.json') as f:
            self.sales = json.load(f)

    def save_resources(self):
        with open('data/resources.json', 'w') as f:
            json.dump(self.resources, f, indent=2)

    def save_sales(self):
        with open('data/sales.json', 'w') as f:
            json.dump(self.sales, f, indent=2)

    def show_menu(self):
        for drink, details in self.resources['menu'].items():
            print(f"{drink.title()}: Rs.{details['cost']}")

    def is_available(self, drink):
        if drink not in self.resources['menu']:
            return False
        recipe = self.resources['menu'][drink]
        for item in ['water', 'milk', 'coffee']:
            if recipe[item] > self.resources[item]:
                print(f"Not enough {item}")
                return False
        return True

    def make_drink(self, drink):
        recipe = self.resources['menu'][drink]
        for item in ['water', 'milk', 'coffee']:
            self.resources[item] -= recipe[item]
        self.sales['total_sales'] += recipe['cost']
        self.save_resources()
        self.save_sales()
        print(f"{drink.title()} is ready! ")
