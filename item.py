"""
    Author: 2d Lt Anthony Tolbert
    Course: CSCE086
    Air Force Institute of Technology


    Implementation of an inventory item for commercial settings.

    This module has no external dependencies
"""


class OutOfStock(Exception):
    pass


class Item:
    """
    Commercial item with inventory control

    This class has 4 attributes and 1 method

    Attributes
    ----------
    * price:        A float storing how much an item costs
    * inventory:    An integer count of how many of the item have not yet been sold
    * id:           A unique identification number for the item type
    * name:         The items plain text name

    Methods
    ------
    * buy: Completes a transaction if there is enough stock in the inventory
    """

    def __init__(self, idd: int, name: str, price: float = .50, inventory: int = 1):
        # Added case for $ included in price
        try:
            if price[0] == '$':
                price = price[1:]
        except TypeError:
            pass
        self.price = float(price)
        self.inventory = int(inventory)
        self.id = idd
        self.name = name

    def __str__(self):
        return f'{self.name}({self.id}): {self.inventory}, costs: ${self.price:.2f}'

    def buy(self):
        """Completes a transaction if there is enough stock in the inventory"""
        if self.inventory > 0:
            self.inventory -= 1
        else:
            raise OutOfStock(f'{self.name} is out of stock!')
