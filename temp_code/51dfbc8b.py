class BankAccount:
    def __init__(self, name, acc_no, balance):
        self.name = name
        self.acc_no = acc_no
        self.__balance = balance   # private variable

    def deposit(self, amount):
        self.__balance += amount
        print("Amount Deposited:", amount)

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient Balance")
        else:
            self.__balance -= amount
            print("Amount Withdrawn:", amount)

    def check_balance(self):
        print("Current Balance:", self.__balance)

    def display(self):
        print("Account Holder:", self.name)
        print("Account Number:", self.acc_no)


class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter Name: ")
        acc_no = input("Enter Account Number: ")
        balance = float(input("Enter Initial Balance: "))
        account = BankAccount(name, acc_no, balance)
        self.accounts[acc_no] = account
        print("Account Created Successfully")

    def deposit_money(self):
        acc_no = input("Enter Account Number: ")
        if acc_no in self.accounts:
            amount = float(input("Enter Amount: "))
            self.accounts[acc_no].deposit(amount)
        else:
            print("Account Not Found")

    def withdraw_money(self):
        acc_no = input("Enter Account Number: ")
        if acc_no in self.accounts:
            amount = float(input("Enter Amount: "))
            self.accounts[acc_no].withdraw(amount)
        else:
            print("Account Not Found")

    def check_balance(self):
        acc_no = input("Enter Account Number: ")
        if acc_no in self.accounts:
            self.accounts[acc_no].check_balance()
        else:
            print("Account Not Found")


bank = BankSystem()

while True:
    print("\n--- BANK MANAGEMENT SYSTEM ---")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        bank.create_account()

    elif choice == "2":
        bank.deposit_money()

    elif choice == "3":
        bank.withdraw_money()

    elif choice == "4":
        bank.check_balance()

    elif choice == "5":
        print("Thank You")
        break

    else:
        print("Invalid Choice")