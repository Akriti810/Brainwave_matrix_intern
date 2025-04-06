class ATM:
    def __init__(self):
        self.users = {
            '1234': {'pin': '1111', 'balance': 5000, 'transactions': []},
            '5678': {'pin': '2222', 'balance': 3000, 'transactions': []}
        }
        self.current_user = None

    def authenticate_user(self):
        card_number = input("Enter your card number: ")
        pin = input("Enter your PIN: ")
        user = self.users.get(card_number)

        if user and user['pin'] == pin:
            self.current_user = card_number
            print("\n Login successful!\n")
            return True
        else:
            print(" Invalid card number or PIN.\n")
            return False

    def check_balance(self):
        balance = self.users[self.current_user]['balance']
        print(f" Your current balance is: ${balance}")

    def withdraw_cash(self):
        try:
            amount = float(input("Enter withdrawal amount: "))
            if 0 < amount <= self.users[self.current_user]['balance']:
                self.users[self.current_user]['balance'] -= amount
                self.users[self.current_user]['transactions'].append(f"Withdrew ${amount}")
                print(f" Withdrawn ${amount}. New balance: ${self.users[self.current_user]['balance']}")
            else:
                print(" Insufficient funds or invalid amount.")
        except ValueError:
            print(" Invalid input. Please enter a number.")

    def deposit_cash(self):
        try:
            amount = float(input("Enter deposit amount: "))
            if amount > 0:
                self.users[self.current_user]['balance'] += amount
                self.users[self.current_user]['transactions'].append(f"Deposited ${amount}")
                print(f" Deposited ${amount}. New balance: ${self.users[self.current_user]['balance']}")
            else:
                print(" Deposit amount must be greater than zero.")
        except ValueError:
            print(" Invalid input. Please enter a number.")

    def show_transactions(self):
        print("\n Transaction History:")
        transactions = self.users[self.current_user]['transactions']
        if transactions:
            for tx in transactions:
                print(f" - {tx}")
        else:
            print("No transactions available.")

    def logout(self):
        print(" Logging out...")
        self.current_user = None

    def run(self):
        if not self.authenticate_user():
            return

        while True:
            print("\n ATM Menu:")
            print("1. Check Balance")
            print("2. Withdraw Cash")
            print("3. Deposit Cash")
            print("4. Transaction History")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.withdraw_cash()
            elif choice == '3':
                self.deposit_cash()
            elif choice == '4':
                self.show_transactions()
            elif choice == '5':
                self.logout()
                break
            else:
                print("Invalid choice. Try again.")

# Run the ATM system
if __name__ == "__main__":
    atm = ATM()
    atm.run()
