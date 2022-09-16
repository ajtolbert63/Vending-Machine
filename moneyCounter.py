class MoneyCounter:
    def __init__(self):
        self.balance_available = 0  # in cents

    def change(self, price):
        c = self.balance_available - price
        ret = '$' + f'{c:.2f}'
        c *= 100  # Convert to cents
        o = round(c // 100, 2)
        c -= o * 100
        q = round(c // 25, 2)
        c -= q * 25
        d = round(c // 10, 2)
        c -= d * 10
        n = round(c // 5, 2)
        c -= n * 5
        p = round(c, 2)
        c -= p
        self.balance_available = 0
        return [o, q, d, n, p], ret

    def balance(self, coins):
        c = 0
        if type(coins) != list or len(coins) != 5:
            raise TypeError
        o, q, d, n, p = coins
        c += int(o) * 100
        c += int(q) * 25
        c += int(d) * 10
        c += int(n) * 5
        c += int(p)
        self.balance_available = c / 100
