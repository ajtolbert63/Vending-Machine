class MoneyCounter:
    def __init__(self):
        self.balance_available = 0  # in cents

    def change(self, price):
        c = self.balance_available - price
        ret = '$' + f'{c:.2f}'
        c *= 100  # Convert to cents
        o = c // 100
        c -= o * 100
        q = c // 25
        c -= q * 25
        d = c // 10
        c -= d * 10
        n = c // 5
        c -= n * 5
        p = c
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
