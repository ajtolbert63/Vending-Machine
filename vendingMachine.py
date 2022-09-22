"""
    Author: 2d Lt Anthony Tolbert
    Course: CSCE086
    Air Force Institute of Technology


    Implementation of a vending machine that can be interacted with via a commandline prompt.
    Syntax instructions and command definitions can be found by running VendingMachine.help()

    This module requires:
    * re
    * item
    * moneyCounter
"""
import re
import item
import moneyCounter


class ItemNotFound(Exception):
    pass


class VendingMachine:
    """
    Command Line Based Vending Machine

    The user can interact with the vending machine via the command line.
    This is done using a list of supported functions available via the self.help() function.
    To enter interact with the vending machine use the self.input() function

    This class has 4 attributes and 7 methods

    Attributes
    ----------
    * items:        A dictionary of items in the inventory keyed by the item's name
    * history_list: A list of successfully completed transaction commands as inputted by the user
    * mc:           An instance of the MoneyCounter class. This deals with most of the math involved in transactions
    * next_ID:      An int to be assigned as the unique ID number to the next item added to the inventory

    Methods
    -------
    input:
    _buy:
    _add:
    _inventory:
    help:
    _history:

    """

    def __init__(self):
        self.items = {}
        self.history_list = []
        self.mc = moneyCounter.MoneyCounter()
        self.next_ID = 0

    def input(self):
        """
        Continual loop that gets user input and checks it against valid commands,
         then executes those commands as appropriate
        """
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

    def _buy(self, args: list, usr_in: str):
        """
        Functionality for purchasing an item from the vending machine

        First checks for multi-word item name,
         then checks to see if item is in the inventory,
         finally completes the purchase via the money counter

        :param args: usr input string split into list of strings
        :param usr_in: raw string of user input
        """
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

    def _add(self, args: list, usr_in: str):
        """
        Adds a new item to the inventory or updates an existing item's stock

        First checks for multi-word item names
         Then checks if item is already in the inventory
         If not it is added by creating a new entry in the items dictionary
         If it is the properties of the item are updated

        :param args: usr input string split into list of strings
        :param usr_in: raw string of user input
        """
        args[2] = re.findall('(?<=item)(.*?)(?=[0-9])', usr_in)[0].strip()
        for i in range(len(args[2].split()) - 1):
            args.pop(3 + i)
        try:
            if args[1] == 'item':
                if self.items.get(args[2]) is None:
                    self.items[args[2]] = item.Item(self.next_ID, args[2], args[4], args[3])
                    self.next_ID += 1
                    print(f'Successfully added item {self.items[args[2]]}')
                else:
                    self.items[args[2]].inventory += args[3]
                    self.items[args[2]].price = args[4]
                    print(f'Successfully updated item {self.items[args[2]]}')
                self.history_list.append(usr_in)
            else:
                raise IndexError
        except IndexError:
            print('Invalid input')

    def _inventory(self):
        """
        Prints the inventory of the vending machine using the __str__ method of the item class

        Iterates of the self.items dictionary and prints items.
        Or indicates the inventory is empty if that is true
        """
        # print('Name(ID) #in stock, price')
        if self.items:
            for i in self.items:
                print(self.items[i])
        else:
            print('the inventory is empty')

    @staticmethod
    def help():
        """Display list of available commands to the user"""
        print('''
balance                         shows the balance of the vending machine                              
history                         prints list of transactions                          
inventory                       prints current inventory (name, id, price, count)                          
add item <str> <int> <float>    add item to inventory
buy item <str> {5}<int>         immediately buy item with provided coins
help                            display this help message                              
exit                            exit the vending machine                              
''')

    def _history(self):
        """Print a list of successful transactions completed during the session"""
        if self.history_list:
            for command in self.history_list:
                print(command)
        else:
            print('no transaction history')


if __name__ == '__main__':
    vm = VendingMachine()
    vm.input()
