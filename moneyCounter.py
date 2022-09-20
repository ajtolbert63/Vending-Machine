class InsufficientFunds(Exception):
    pass


class MoneyCounter:

    def __init__(self, o=5, q=5, d=5, n=5, p=5):
        self.balance_available = 0
        self.dollars = o
        self.quarters = q
        self.dimes = d
        self.nickels = n
        self.pennies = p

        self.update_balance()
        self.__INIT_BALANCE = self.balance_available

    def change(self, due):
        """

        param due: money due to user in cents
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
            print("Sorry not enough change in the machine")
            print(
                f'you got ${(og_due - due) / 100 :.2f} ({round(o)} dollars, {round(q)} quarters, {round(d)} dimes, '
                f'{round(n)} nickels, {round(p)} pennies)')
            print(f'missing ${due / 100:.2f} of ${og_due / 100:.2f} due')
            return

        print(
            f'change: ${og_due / 100:.2f} {round(o)} dollars, {round(q)} quarters, {round(d)} dimes, '
            f'{round(n)} nickels, {round(p)} pennies')

    def update_balance(self):
        c = 0
        c += int(self.dollars) * 100
        c += int(self.quarters) * 25
        c += int(self.dimes) * 10
        c += int(self.nickels) * 5
        c += int(self.pennies)
        self.balance_available = c / 100

    def print_balance(self):
        print(f'There is: ${self.balance_available:.2f} in the machine')
        if self.balance_available >= self.__INIT_BALANCE:
            print(f'${self.balance_available - self.__INIT_BALANCE:.2f} has been profited')
        else:
            print(f'{self.__INIT_BALANCE - self.balance_available} has been lost')

    def purchase(self, price: float, coins: list):
        """
        Given the price of an item, and currency to buy the item
        Add the currency to inventory

        param price: in dollars
        param coins: list of currency entered
        """
        if type(coins) != list or len(coins) != 5:
            raise TypeError
        o, q, d, n, p = coins
        c = count(coins)
        if c < price * 100:
            raise InsufficientFunds(f"InsufficientFunds! Need ${-1 * (c / 100 - price):.2f} more")
        # Add coins to machines inventory
        self.dollars += int(o)
        self.quarters += int(q)
        self.dimes += int(d)
        self.nickels += int(n)
        self.pennies += int(p)

        price *= 100  # Convert to cents

        self.change(c - price)  # Calculate change due
        self.update_balance()  # update balance of machine


def count(coins):
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
