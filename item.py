class OutOfStock(Exception):
    pass


class Item:
    def __init__(self, idd, name, price=.50, inventory=1):
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
        if self.inventory > 0:
            self.inventory -= 1
        else:
            raise OutOfStock
