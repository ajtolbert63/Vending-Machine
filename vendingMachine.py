import item
import moneyCounter


class ItemNotFound(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class VendingMachine:

    def __init__(self):
        self.items = {}
        self.total_items = 0
        self.history_list = []
        self.mc = moneyCounter.MoneyCounter()
        self.newID = 0
        self.cart = []

    def input(self):
        while True:
            # TODO: Change history to list of transactions
            usr_in = input('VendingMachine>')
            args = usr_in.split()
            match args[0]:
                case 'history':
                    self._history()
                case 'balance':
                    print(f'${self.mc.balance_available:.2f}')
                case 'inventory':
                    self._inventory()
                case 'add':
                    self._add(args, usr_in)
                case 'buy':
                    # TODO: add case for just adding money
                    self._buy(args, usr_in)
                case 'help':
                    self.help()
                case 'exit':
                    self.done()
                    break
                case _:
                    print(f'\'usr_in\' is not a valid command')
                    self.help()

    def _buy(self, args, usr_in):
        args[4] = args[3:8]
        try:
            i = self.items.get(args[2])
            if i is None:
                raise ItemNotFound(f'No item \'{args[1]}\' found in inventory')
        except ItemNotFound as e:
            print(e)
            return
        try:
            self.mc.balance(args[4])
            if self.mc.balance_available - i.price >= 0:
                i.buy()
                self.history_list.append(usr_in)
                print(self.mc.change(i.price))
            else:
                raise InsufficientFunds(f"need {-1 * (self.mc.balance_available - i.price)} more")
        except InsufficientFunds as e:
            print(e)

    def _add(self, args, usr_in):
        try:
            if args[1] == 'item':
                if self.items.get(args[2]) is None:
                    self.items[args[2]] = item.Item(self.newID, args[2], args[4], args[3])
                    self.newID += 1
                else:
                    self.items[args[2]].inventory += args[3]
                    self.items[args[2]].price = args[4]
                self.history_list.append(usr_in)
        except IndexError:
            print('Invalid input')
            self._done()

    def _inventory(self):
        # print('Name (ID)\tPrice\tCount')
        for i in self.items:
            print(self.items[i])
            break
        else:
            print('the inventory is empty')

    @staticmethod
    def help():
        print('''
balance                         shows the balance of the current transaction                               
history                         prints list of commands                           
inventory                       prints current inventory (name, id, price, count)                          
add item <str> <int> <float>    add item to inventory
buy item <str> {5}<int>         immediately buy item with provided coins
help                            display this help message                              
exit                            exit the vending machine                              
''')

    def _history(self):
        self.history_list.reverse()
        for command in self.history_list:
            print(command)
            break
        else:
            print('no transaction history')
        self.history_list.reverse()

    def _done(self):
        # TODO: return balance and clear for new events
        print(self.mc.change(0))
        self.items.clear()
        self.cart.clear()


if __name__ == '__main__':
    vm = VendingMachine()
    vm.input()
