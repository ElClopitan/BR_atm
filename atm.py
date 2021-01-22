class Bank:
    def __init__(self):
        self.data = {}

    # Checks in card is in bank
    # card number
    def check_card(self, card):
        return card in self.data

    # Checks if the pin is correct for the card
    # card number, pin number
    def check_pin(self, card, pin):
        if not self.check_card(card):
            return f"Sorry, card {card} is not a member of this bank. Please add as a member or try a different card. Thank you."
        return self.data[card]['pin'] == pin

    # Adds a new member to the Bank
    # card number, pin number, account number/name, amount of money to add
    def add_member(self, card, pin, account, money):
        retStr = ''
        if self.check_card(card):
            self.data[card]['accounts'][account] = self.data[card]['accounts'].get(account, 0) + money
            retStr = f"Successfully added amount {money} to account {account} on card {card}."
        else:
            self.data[card] = {'pin': pin, 'accounts':{account:money}}
            retStr = f"Successfully added card {card} to bank."
        return retStr

    # Adds an account to an existing member of the Bank or, if account already exists, adds money to the account
    # card number, pin number, account number/name, amount of money to add
    def add_account(self,card, pin, account, money):
        retStr = ''
        if not self.check_card(card):
            retStr = f"Sorry, card {card} is not a member of this bank. Please add as a member or try a different card. Thank you."
        else:
            retStr = self.add_member(card, pin, account, money)
        return retStr

    # Update accounts for card
    # card number, accounts
    def update_accounts(self, card, accounts):
        self.data[card]['accounts'] = accounts

class ATM:
    # Initialize with a preexisiting bank and some amount of money in the ATM
    def __init__(self, bank, money):
        self.bank = bank
        self.reserve = money
        self.curr_card = None
        self.curr_pin = None
        self.curr_user = None

    # Inserting a card
    # card number, pin number
    def insert_card(self, card, pin):
        retStr = ''
        if self.curr_user:
            return False, "There is already a user logged in. Please use another one of our machines. Thank you."
        valid = self.bank.check_pin(card, pin)
        if type(valid) == bool:
            if valid:
                self.curr_card = card
                self.cur_pin = pin
                self.curr_user = self.bank.data[card]['accounts']
                retStr = valid, "Welcome back! Please take back your card."
            else:
                retStr = valid, "Invalid pin. Please try again."
        else:
            retStr = False, retStr
        return retStr

    # Check names of accounts
    def check_accounts(self):
        retStr = ''
        if self.curr_user:
            retStr = True, str(self.curr_user.keys())
        else:
            retStr = False, "Error. No User logged in."
        return retStr

    # Selects account
    # account number/name
    def select_account(self, account):
        retStr = ''
        if self.curr_user:
            retStr = True, account in self.curr_user
        else:
            retStr = False, "Error. No User logged in."
        return retStr

    # Check balance of an account
    # account number/name
    def check_balance(self, account):
        retStr = ''
        try:
            if self.curr_user:
                retStr = True, f"Current balance on account {account} is {self.curr_user[account]}.", self.curr_user[account]
            else:
                retStr = False, "Error. No User logged in."
        except:
            retStr = False, f"Invalid account {account}."
        return retStr

    # Deposit money in account
    # account number/name, money to deposit
    def deposit(self, account, money):
        retStr = ''
        try:
            self.curr_user[account] += money
            self.reserve += money
            retStr = True, f"Deposited amount {money} into account {account}.", self.curr_user[account]
        except:
            retStr = False, f"Invalid account {account}."
        return retStr

    # Withdraw money from account
    # account number/name, money to withdraw
    def withdraw(self, account, money):
        retStr = ''
        try:
            if money > self.curr_user[account]:
                retStr = False, f"Not enough funds in account {account}."
            else:
                self.curr_user[account] -= money
                retStr = True, f"Amount {money} withdrawn from account {account}. Dispensing now.", self.curr_user[account]
        except:
            retStr = False, f"Invalid account {account}."
        return retStr

    # Actions after inserting card
    # Withdraw/Deposit/Check Balance/Select Account/Check Accounts/Logoff, account number/name, money
    def action(self, action, account=None, money=0):
        retStr = ''
        action = action.lower()
        if type(money) != int:
            return "Invalid amount entered. Please try again."
        if action == "withdraw":
            if money <= 0:
                retStr = False, f"Amount {money} is not a valid amount to withdraw. Please enter an amount greater than 0"
            elif money > self.reserve:
                retStr = False, f"Amount {money} is more than the current reserve in this ATM. We apologize for the inconvenience"
            else:
                retStr = self.withdraw(account, money)
                # self.dispense(money) # Call to physically dispense money not implemented
                self.reserve -= money
        elif action == "deposit":
            if money <= 0:
                retStr = False, f"Amount {money} is not a valid amount to deposit. Please enter an amount greater than 0"
            else:
                retStr = self.deposit(account, money)
        elif action == "check balance":
            retStr = self.check_balance(account)
        elif action == "select account":
            retStr = self.select_account(account)
        elif action == "check accounts":
            retStr = self.check_accounts()
        elif action == "logoff":
            self.bank.update_accounts(self.curr_card, self.curr_user)
            self.card = None
            self.pin = None
            self.curr_user = None
            retStr = True, "Thank you for using our services. We hope to see you soon!"
        else:
            retStr = False, f"Invalid action {action}. Please try again."
        return retStr

if __name__ == "__main__":
    bank = Bank()

    atm0 = ATM(bank, 0)
    check, _ = atm0.insert_card(0, 0)
    if check:
        print('Test Invalid Insert - FAIL')
    else: print('Test Invalid Insert - PASS')

    bank.add_member(1, 1234, 'first', 100)
    bank.add_account(1, 1234, 'second', 1000)
    bank.add_member(2, 2345, 'first', 100)
    atm1 = ATM(bank, 1100)
    correct_reponses = {1: [False, True, True, True, 100, 1000, False, 0, 0, False, True],
                        2: [True, False, True, False, 100, False, False, False, False, False, 1100, True, True]}
    results = []
    for i in [1,2]:
        check0 = atm1.insert_card(i, 2345)[0]
        check1 = atm1.insert_card(i, 1234)[0]
        check2 = atm1.action("Select Account", 'first')[1]
        check3 = atm1.action("Select Account", 'second')[1]
        check4 = atm1.action("check Balance", 'first')[2]
        check5 = atm1.action("check Balance", 'second')[2] if i == 1 else atm1.action("Check Balance", 'second')[0]
        check6 = atm1.action("Withdraw", 'first')[0]
        check7 = atm1.action("Withdraw", 'first', 100)[2] if i == 1 else atm1.action("Check Balance", 'second')[0]
        check8 = atm1.action("Withdraw", 'second', 1000)[2] if i == 1 else atm1.action("Check Balance", 'second')[0]
        check9 = atm1.action("Gimme Money")[0]
        check10 = atm1.action("LogOff")[0] if i == 1 else atm1.action("Deposit", 'first', 1000)[2]
        check11 = atm1.action("Withdraw", 'first', 500)[0]
        check12 = atm1.action("LoGoFf")[0]
        if i == 1:
            checks = [check0, check1, check2, check3, check4, check5, check6, check7, check8, check9, check10]
            results.append([checks[j] == correct_reponses[i][j] for j in range(11)])
        else:
            checks = [check0, check1, check2, check3, check4, check5, check6, check7, check8, check9, check10, check11, check12]
            results.append([checks[j] == correct_reponses[i][j] for j in range(13)])
    print(results)
