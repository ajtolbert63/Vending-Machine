import re
import item
import moneyCounter


class ItemNotFound(Exception):
    pass


class VendingMachine:

    def __init__(self):
        self.items = {}
        self.history_list = []
        self.mc = moneyCounter.MoneyCounter()
        self.next_ID = 0

    def input(self):
        while True:
            usr_in = input('VendingMachine>')
            args = usr_in.split()
            if not args:
                continue

            match args[0]:
                case 'history':
                    self._history()
                case 'balance':
                    self.mc.print_balance()
                case 'inventory':
                    self._inventory()
                case 'add':
                    try:
                        self._add(args, usr_in)
                    except ValueError as e:
                        print(e)
                        self.help()
                        continue
                case 'buy':
                    try:
                        self._buy(args, usr_in)
                    except (ItemNotFound, item.OutOfStock, moneyCounter.InsufficientFunds) as e:
                        print(e)
                        continue
                case 'help':
                    self.help()
                case 'exit':
                    break
                case _:
                    print(f'\'{usr_in}\' is not a valid command')
                    self.help()

    def _buy(self, args, usr_in):
        args[2] = re.findall('(?<=item)(.*?)(?=[0-9])', usr_in)[0].strip()
        for i in range(len(args[2].split()) - 1):
            args.pop(3 + i)
        args[3] = args[3:8]  # coin list

        i = self.items.get(args[2])
        if i is None:
            raise ItemNotFound(f'No item \'{args[2]}\' found in inventory')
        self.mc.purchase(i.price, args[3])
        i.buy()
        self.history_list.append(usr_in)

    def _add(self, args, usr_in):
        args[2] = re.findall('(?<=item)(.*?)(?=[0-9])', usr_in)[0].strip()
        for i in range(len(args[2].split()) - 1):
            args.pop(3 + i)
        try:
            if args[1] == 'item':
                if self.items.get(args[2]) is None:
                    self.items[args[2]] = item.Item(self.next_ID, args[2], args[4], args[3])
                    self.next_ID += 1
                else:
                    self.items[args[2]].inventory += args[3]
                    self.items[args[2]].price = args[4]
                self.history_list.append(usr_in)
            else:
                raise IndexError
        except IndexError:
            print('Invalid input')

    def _inventory(self):
        # print('Name(ID) #in stock, price')
        if self.items:
            for i in self.items:
                print(self.items[i])
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
        if self.history_list:
            for command in self.history_list:
                print(command)
        else:
            print('no transaction history')


if __name__ == '__main__':
    vm = VendingMachine()
    vm.input()
