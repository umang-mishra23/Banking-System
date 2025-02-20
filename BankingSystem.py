import random
import time
from datetime import datetime

class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = {}
    
    def create_account(self, account_holder, initial_balance, pin):
        account_number = self.generate_account_number()
        account = BankAccount(account_number, account_holder, initial_balance, pin)
        self.accounts[account_number] = account
        self.transactions[account_number] = []
        return account

    def generate_account_number(self):
        return "".join(random.choice("0123456789") for _ in range(8))

    def get_account(self, account_number, pin=None):
        account = self.accounts.get(account_number)
        if account and (pin is None or account.pin == pin):
            return account
        return None
    
    def perform_transaction(self, account_number, transaction_type, amount, pin):
        account = self.get_account(account_number, pin)
        if not account:
            return "Account not found or incorrect PIN."

        if transaction_type == "deposit":
            account.deposit(amount)
        elif transaction_type == "withdraw":
            if not account.withdraw(amount):
                return "Insufficient funds."
        else:
            return "Invalid transaction type."

        self.transactions[account_number].append((transaction_type, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return "Transaction completed successfully."

    def get_transaction_history(self, account_number, pin):
        account = self.get_account(account_number, pin)
        if not account:
            return "Invalid account number or PIN."
        return self.transactions.get(account_number, [])

class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance, pin):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.pin = pin
        self.interest_rate = 0.02  # 2% Annual Interest Rate

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self, pin):
        if self.pin == pin:
            return self.balance
        return "Incorrect PIN."
    
    def apply_interest(self):
        self.balance += self.balance * self.interest_rate

def main():
    bank = Bank()

    while True:
        print("\nPython Banking System")
        print("1. Create Account")
        print("2. Perform Transaction")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Apply Interest")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            account_holder = input("Enter your name: ")
            initial_balance = float(input("Enter initial balance: "))
            pin = input("Set a 4-digit PIN: ")
            if len(pin) != 4 or not pin.isdigit():
                print("Invalid PIN format. Must be 4 digits.")
                continue
            account = bank.create_account(account_holder, initial_balance, pin)
            print(f"Account created successfully! Account Number: {account.account_number}")

        elif choice == "2":
            account_number = input("Enter account number: ")
            pin = input("Enter PIN: ")
            transaction_type = input("Enter transaction type (deposit/withdraw): ").lower()
            amount = float(input("Enter transaction amount: "))
            result = bank.perform_transaction(account_number, transaction_type, amount, pin)
            print(result)

        elif choice == "3":
            account_number = input("Enter account number: ")
            pin = input("Enter PIN: ")
            account = bank.get_account(account_number, pin)
            if account:
                print(f"Account Balance: RS.{account.get_balance(pin)}")
            else:
                print("Invalid account number or PIN.")

        elif choice == "4":
            account_number = input("Enter account number: ")
            pin = input("Enter PIN: ")
            transactions = bank.get_transaction_history(account_number, pin)
            if isinstance(transactions, str):
                print(transactions)
            elif transactions:
                print("Transaction History:")
                for trans_type, amount, timestamp in transactions:
                    print(f"{trans_type.capitalize()} ${amount} on {timestamp}")
            else:
                print("No transactions found.")

        elif choice == "5":
            account_number = input("Enter account number: ")
            pin = input("Enter PIN: ")
            account = bank.get_account(account_number, pin)
            if account:
                account.apply_interest()
                print("Interest applied successfully.")
            else:
                print("Invalid account number or PIN.")

        elif choice == "6":
            print("Exiting the Python Banking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
