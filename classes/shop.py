'''
shop.py
Defines the Shop class for managing item transactions in the game
'''

class Shop:
    def __init__(self):
        #  shop's inventory with items and their prices
        self.inventory = {
            'Axe': {'price': 10},
            'Sword': {'price': 20},
            'Pickaxe': {'price': 15},
            'Apple': {'price': 5},
            'Corn': {'price': 3},
            'Iron': {'price': 8},
            'Copper': {'price': 6},
            'Wood': {'price': 4}
        }

    def buy_item(self, item_name, player):
        if item_name in self.inventory and player.gold >= self.inventory[item_name]['price']:
            player.gold -= self.inventory[item_name]['price']
            player.inventory.append(item_name)
            print(f'You bought {item_name} for {self.inventory[item_name]["price"]} gold.')
        else:
            print('You cannot afford that item.')

    def sell_item(self, item_name, player):
        if item_name in player.inventory:
            player.gold += self.inventory[item_name]['price']
            player.inventory.remove(item_name)
            print(f'You sold {item_name} for {self.inventory[item_name]["price"]} gold.')
        else:
            print('You do not have that item to sell.')
