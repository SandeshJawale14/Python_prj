import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Set up styles for better appearance
style = ttk.Style()

# Configure styles for different widgets
style.configure("TFrame", background="#f8f8f8")
style.configure("TLabel", background="#f8f8f8", font=("Arial", 12, "bold"))
style.configure(
    "TButton",
    font=("Arial", 12, "bold"),
    foreground="#ffffff",
    background="#0078d7",
    width=20,
)
style.map("TButton", background=[("active", "#005a9e")])


# Custom exception for insufficient funds
class InsufficientFundsError(Exception):
    pass


# Account class to manage individual accounts
class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds. Available balance is {self.balance}."
            )
        elif amount > 0:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder}\nBalance: ${self.balance:.2f}"


# Main Banking System Class
class BankingSystem:
    def __init__(self, root):
        self.accounts = {}
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x500")

        # Create a notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=20, expand=True)

        # Tab for creating an account
        self.create_account_tab = tk.Frame(self.notebook, bg="#f8f8f8")
        self.notebook.add(self.create_account_tab, text="Create Account", padding=10)

        # Tab for transactions (Deposit/Withdraw)
        self.transaction_tab = tk.Frame(self.notebook, bg="#f8f8f8")
        self.notebook.add(self.transaction_tab, text="Transactions", padding=10)

        # Tab for account information
        self.info_tab = tk.Frame(self.notebook, bg="#f8f8f8")
        self.notebook.add(self.info_tab, text="Account Info", padding=10)

        # Account Creation Section
        self.acc_num_label = tk.Label(
            self.create_account_tab, text="Account Number:", font=("Arial", 14)
        )
        self.acc_num_label.grid(row=0, column=0, padx=20, pady=10)
        self.acc_num_entry = tk.Entry(
            self.create_account_tab, font=("Arial", 14), width=20
        )
        self.acc_num_entry.grid(row=0, column=1, padx=20, pady=10)

        self.acc_holder_label = tk.Label(
            self.create_account_tab, text="Account Holder:", font=("Arial", 14)
        )
        self.acc_holder_label.grid(row=1, column=0, padx=20, pady=10)
        self.acc_holder_entry = tk.Entry(
            self.create_account_tab, font=("Arial", 14), width=20
        )
        self.acc_holder_entry.grid(row=1, column=1, padx=20, pady=10)

        self.initial_balance_label = tk.Label(
            self.create_account_tab, text="Initial Balance:", font=("Arial", 14)
        )
        self.initial_balance_label.grid(row=2, column=0, padx=20, pady=10)
        self.initial_balance_entry = tk.Entry(
            self.create_account_tab, font=("Arial", 14), width=20
        )
        self.initial_balance_entry.grid(row=2, column=1, padx=20, pady=10)

        self.create_acc_button = tk.Button(
            self.create_account_tab, text="Create Account", command=self.create_account
        )
        self.create_acc_button.grid(row=3, columnspan=2, pady=10)

        # Transaction Section
        self.trans_acc_num_label = tk.Label(
            self.transaction_tab, text="Account Number:", font=("Arial", 14)
        )
        self.trans_acc_num_label.grid(row=0, column=0, padx=20, pady=10)
        self.trans_acc_num_entry = tk.Entry(
            self.transaction_tab, font=("Arial", 14), width=20
        )
        self.trans_acc_num_entry.grid(row=0, column=1, padx=20, pady=10)

        self.amount_label = tk.Label(
            self.transaction_tab, text="Amount:", font=("Arial", 14)
        )
        self.amount_label.grid(row=1, column=0, padx=20, pady=10)
        self.amount_entry = tk.Entry(self.transaction_tab, font=("Arial", 14), width=20)
        self.amount_entry.grid(row=1, column=1, padx=20, pady=10)

        self.deposit_button = tk.Button(
            self.transaction_tab, text="Deposit", command=self.deposit
        )
        self.deposit_button.grid(row=2, column=0, padx=20, pady=10)

        self.withdraw_button = tk.Button(
            self.transaction_tab, text="Withdraw", command=self.withdraw
        )
        self.withdraw_button.grid(row=2, column=1, padx=20, pady=10)

        # Account Information Section
        self.info_acc_num_label = tk.Label(
            self.info_tab, text="Account Number:", font=("Arial", 14)
        )
        self.info_acc_num_label.grid(row=0, column=0, padx=20, pady=10)
        self.info_acc_num_entry = tk.Entry(self.info_tab, font=("Arial", 14), width=20)
        self.info_acc_num_entry.grid(row=0, column=1, padx=20, pady=10)

        self.info_button = tk.Button(
            self.info_tab, text="Display Info", command=self.display_info
        )
        self.info_button.grid(row=1, columnspan=2, pady=10)

    # Account creation method
    def create_account(self):
        acc_num = self.acc_num_entry.get()
        acc_holder = self.acc_holder_entry.get()
        try:
            initial_balance = float(self.initial_balance_entry.get())
            if initial_balance < 0:
                raise ValueError("Initial balance cannot be negative.")
        except ValueError as e:
            messagebox.showwarning(
                "Error", f"Invalid input for initial balance: {str(e)}"
            )
            return

        if acc_num and acc_holder:
            if acc_num in self.accounts:
                messagebox.showwarning("Error", "Account number already exists!")
            else:
                self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
                messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showwarning(
                "Error", "Account number and holder name cannot be empty!"
            )

    # Deposit method
    def deposit(self):
        acc_num = self.trans_acc_num_entry.get()
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            messagebox.showwarning("Error", f"Invalid input: {str(e)}")
            return

        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].deposit(amount)
                messagebox.showinfo(
                    "Success",
                    f"Deposited ${amount:.2f}. New balance is ${self.accounts[acc_num].get_balance():.2f}.",
                )
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Error", "Account not found!")

    # Withdraw method
    def withdraw(self):
        acc_num = self.trans_acc_num_entry.get()
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError as e:
            messagebox.showwarning("Error", f"Invalid input: {str(e)}")
            return

        if acc_num in self.accounts:
            try:
                self.accounts[acc_num].withdraw(amount)
                messagebox.showinfo(
                    "Success",
                    f"Withdrew ${amount:.2f}. New balance is ${self.accounts[acc_num].get_balance():.2f}.",
                )
            except InsufficientFundsError as e:
                messagebox.showwarning("Error", str(e))
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
        else:
            messagebox.showwarning("Error", "Account not found!")

    # Display account information method
    def display_info(self):
        acc_num = self.info_acc_num_entry.get()

        if acc_num in self.accounts:
            account_info = self.accounts[acc_num].display_account_info()
            messagebox.showinfo("Account Info", account_info)
        else:
            messagebox.showwarning("Error", "Account not found!")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystem(root)
    root.mainloop()
