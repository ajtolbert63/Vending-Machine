"""
    Author: 2d Lt Anthony Tolbert
    Course: CSCE086
    Air Force Institute of Technology

    Implements a class that can be used in a commercial setting.
    This module keeps an inventory of american denominations including:
        * dollar bills
        * quarters
        * dimes
        * nickels
        * pennies
    This module also includes an external function to convert
     a list of quantities of dollars and coins to a human-readable value
    This module has no external dependencies
"""


class InsufficientFunds(Exception):
    pass


class MoneyCounter:
    """
    Small setting commercial money module that maintains a money inventory and returns change given the price of an item

    This class has 7 attributes and 4 methods

    Attributes
    ----------
    balance_available:  An amount, in dollars, of money in the machine
    dollars:            An integer count of dollars in the inventory of the money counter
    quarters:           An integer count of quarters in the inventory of the money counter
    dimes:              An integer count of dimes in the inventory of the money counter
    nickels:            An integer count of nickels in the inventory of the money counter
    pennies:            An integer count of pennies in the inventory of the money counter
    __INIT_BALANCE__:   The dollar amount the money counter starts with

    Methods
    -------
    change:         Given an amount of Money due to a user, take that amount from the money counter and return it to
                     the user in the largest denominations possible
    update_balance: Updates the self.balance available attribute by adding the denominations (in cents) then convert to
                     dollars
    print_balance:  Prints the amount of money currently in the money counter and shows profit/loss since it was
                     initialized
    purchase:       Inventory the money from the user and complete the purchase
    """

    def __init__(self, o=5, q=5, d=5, n=5, p=5):
        self.balance_available = 0
        self.dollars = o
        self.quarters = q
        self.dimes = d
        self.nickels = n
        self.pennies = p

        self.update_balance()
        self.__INIT_BALANCE__ = self.balance_available

    def change(self, due: int):
        """
        Given an amount of Money due to a user, take that amount from the money counter and return it to the user
        In the largest denominations possible

        :param due: the amount of money due to the user (in cents)
        """
        og_due = due
        # Dollars
        if due // 100 <= self.dollars:
            self.dollars -= due // 100
            o = (due // 100)
            due -= o * 100
        else:
            o = self.dollars
            due -= o * 100
            self.dollars = 0
        # Quarters
        if due // 25 <= self.quarters:
            self.quarters -= due // 25
            q = (due // 25)
            due -= q * 25
        else:
            q = self.quarters
            due -= q * 25
            self.quarters = 0
        # Dime
        if due // 10 <= self.dimes:
            self.dimes -= due // 10
            d = (due // 10)
            due -= d * 10
        else:
            d = self.dimes
            due -= d * 10
            self.dimes = 0
        # Nickels
        if due // 5 <= self.nickels:
            self.nickels -= due // 5
            n = (due // 5)
            due -= n * 5
        else:
            n = self.nickels
            due -= n * 5
            self.nickels = 0
        # Pennies
        if due <= self.pennies:
            self.pennies -= due
            p = due
            due -= p
        else:
            p = self.pennies
            due -= p
            self.pennies = 0
            # print("Sorry not enough change in the machine")
            # print(
            #     f'you got ${(og_due - due) / 100 :.2f} ({round(o)} dollars, {round(q)} quarters, {round(d)} dimes, '
            #     f'{round(n)} nickels, {round(p)} pennies)')
            # print(f'missing ${due / 100:.2f} of ${og_due / 100:.2f} due')
            raise InsufficientFunds("Sorry not enough change in the machine to complete this transaction\n"
                                    "Please use a more exact amount of change")

        print(
            f'change: ${og_due / 100:.2f} {round(o)} dollars, {round(q)} quarters, {round(d)} dimes, '
            f'{round(n)} nickels, {round(p)} pennies')

    def update_balance(self):
        """Updates the self.balance available attribute by adding the denominations (in cents) then convert to dollar"""
        c = 0
        c += int(self.dollars) * 100
        c += int(self.quarters) * 25
        c += int(self.dimes) * 10
        c += int(self.nickels) * 5
        c += int(self.pennies)
        self.balance_available = c / 100

    def print_balance(self):
        """Prints the amount of money currently in the money counter and shows profit/loss since it was initialized"""
        print(f'There is: ${self.balance_available:.2f} in the machine')
        if self.balance_available >= self.__INIT_BALANCE__:
            print(f'${self.balance_available - self.__INIT_BALANCE__:.2f} has been profited')
        else:
            print(f'{self.__INIT_BALANCE__ - self.balance_available} has been lost')

    def purchase(self, price: float, coins: list):
        """
        Inventory the money from the user and complete the purchase

        Given the price of an item, and currency to buy the item
        Check that there is enough money to complete the transaction
        Add the currency to inventory
        return change to the user

        :param price: in dollars
        :param coins: list of currency entered
        """
        if type(coins) != list or len(coins) != 5:
            raise TypeError
        o, q, d, n, p = coins
        price = int(price * 100)
        c = count(coins)
        if c < price:
            raise InsufficientFunds(f"InsufficientFunds! Need ${-1 * (c - price) / 100:.2f} more")

        # Add coins to machines inventory
        self.dollars += int(o)
        self.quarters += int(q)
        self.dimes += int(d)
        self.nickels += int(n)
        self.pennies += int(p)

        try:
            self.change(c - price)
        except InsufficientFunds as e:  # Catches case where machine may not have enough change to return
            print(e)
            self.change(c)
            raise InsufficientFunds
        self.update_balance()  # update balance of machine


def count(coins: list):
    """
    Given a list of quantities of denominations, return the value in dollars

    :param coins:
    :return:int value of coins & dollars in cents
    """
    if type(coins) != list or len(coins) != 5:
        raise TypeError
    o, q, d, n, p = coins
    # Get total cents added
    c = 0
    c += int(o) * 100
    c += int(q) * 25
    c += int(d) * 10
    c += int(n) * 5
    c += int(p)
    return c
