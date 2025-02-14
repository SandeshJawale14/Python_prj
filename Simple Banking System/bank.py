class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance is {self.balance}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

class Transaction:
    def __init__(self, transaction_id, from_account, to_account, amount):
        self.transaction_id = transaction_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def execute(self):
        try:
            self.from_account.withdraw(self.amount)
            self.to_account.deposit(self.amount)
            print(f"Transaction {self.transaction_id} executed successfully.")
        except InsufficientFundsError as e:
            print(f"Transaction {self.transaction_id} failed: {e}")

# Example usage
if __name__ == "__main__":
    acc1 = Account("12345", "Alice", 1000)
    acc2 = Account("67890", "Bob", 500)

    print(f"Initial balance of Alice's account: {acc1.get_balance()}")
    print(f"Initial balance of Bob's account: {acc2.get_balance()}")

    try:
        acc1.deposit(200)
        acc1.withdraw(1500)
    except InsufficientFundsError as e:
        print(e)

    transaction = Transaction("T001", acc1, acc2, 300)
    transaction.execute()

    print(f"Final balance of Alice's account: {acc1.get_balance()}")
    print(f"Final balance of Bob's account: {acc2.get_balance()}")
