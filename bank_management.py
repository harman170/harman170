# ==========================================
# 🏦 Bank Management System (Python Console App)
# Developer: Harmanjot Kaur
# ==========================================

import json
import random
import string
from pathlib import Path

class Bank:
    database = "data.json"
    data = []

    # Load persistent data at startup
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                data = json.loads(fs.read())
        except Exception:
            data = []

    @classmethod
    def _update_db(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @classmethod
    def _generate_account_number(cls):
        letters = random.choices(string.ascii_uppercase, k=3)
        digits = random.choices(string.digits, k=4)
        combined = letters + digits
        random.shuffle(combined)
        return "".join(combined)

    def create_account(self):
        name = input("Enter full name: ")
        try:
            age = int(input("Enter age: "))
        except ValueError:
            print("Error: Invalid age. Please enter a number.")
            return

        if age < 18:
            print("Error: Account holder must be 18 or older.")
            return

        email = input("Enter email address: ")
        pin = input("Set a 4-digit security PIN: ")

        if len(pin) != 4 or not pin.isdigit():
            print("Error: PIN must be exactly 4 digits.")
            return

        acc_num = self._generate_account_number()
        new_account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": acc_num,
            "balance": 0.0
        }

        Bank.data.append(new_account)
        Bank._update_db()
        print(f"\nAccount created successfully! Account No: {acc_num}")

    def _find_user(self, acc_num, pin):
        for acc in Bank.data:
            if acc["account_number"] == acc_num and acc["pin"] == pin:
                return acc
        return None

    def deposit_money(self):
        acc_num = input("Enter account number: ")
        pin = input("Enter 4-digit PIN: ")
        user = self._find_user(acc_num, pin)

        if not user:
            print("Invalid account number or PIN.")
            return

        try:
            amount = float(input("Enter deposit amount: "))
        except ValueError:
            print("Error: Invalid amount entered.")
            return

        if 0 < amount <= 50000:
            user["balance"] += amount
            Bank._update_db()
            print(f"Success! Deposited: Rs. {amount}. New Balance: Rs. {user['balance']}")
        else:
            print("Invalid deposit amount (Limit: Rs. 1 to Rs. 50,000)")

    def withdraw_money(self):
        acc_num = input("Enter account number: ")
        pin = input("Enter 4-digit PIN: ")
        user = self._find_user(acc_num, pin)

        if not user:
            print("Invalid account no. or PIN.")
            return

        try:
            amount = float(input("Enter withdrawal amount: "))
        except ValueError:
            print("Error: Invalid amount entered.")
            return

        if amount > user["balance"]:
            print("Insufficient account balance.")
        elif amount <= 0:
            print("Withdrawal amount must be greater than ZERO.")
        else:
            user["balance"] -= amount
            Bank._update_db()
            print(f"Success! Withdrawn: Rs. {amount}, Remaining Balance: Rs. {user['balance']}")

    def show_details(self):
        acc_num = input("Enter account number: ")
        pin = input("Enter 4-digit PIN: ")
        user = self._find_user(acc_num, pin)

        if not user:
            print("Invalid account number or PIN.")
            return

        print("\n--- Account Details ---")
        for key, value in user.items():
            if key != "pin":
                print(f"{key.replace('_', ' ').capitalize()}: {value}")

# Main Interactive CLI Menu
def main():
    system = Bank()
    while True:
        print("\n==== Bank Management System ====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Show Account Details")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        if choice == "1":
            system.create_account()
        elif choice == "2":
            system.deposit_money()
        elif choice == "3":
            system.withdraw_money()
        elif choice == "4":
            system.show_details()
        elif choice == "5":
            print("Thank you for using banking system. Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
