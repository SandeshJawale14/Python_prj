class Account:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Insufficient balance or invalid amount.")

    def get_balance(self):
        return self.balance

    def display_details(self):
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder: {self.account_holder}")
        print(f"Balance: {self.balance}")


class Transaction:
    def __init__(self, account, transaction_type, amount):
        self.account = account
        self.transaction_type = transaction_type
        self.amount = amount

    def execute(self):
        if self.transaction_type == "deposit":
            self.account.deposit(self.amount)
        elif self.transaction_type == "withdraw":
            self.account.withdraw(self.amount)
        else:
            print("Invalid transaction type.")


# Example usage
account = Account("123456789", "John Doe", 1000)

# Display account details
account.display_details()

# Perform transactions
deposit_transaction = Transaction(account, "deposit", 500)
deposit_transaction.execute()

withdraw_transaction = Transaction(account, "withdraw", 200)
withdraw_transaction.execute()

# Display updated account details
account.display_details()
