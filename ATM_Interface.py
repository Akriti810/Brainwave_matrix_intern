class ATM:
    def __init__(self, input_func=None):
        self.users = {
            '1234': {'pin': '1111', 'balance': 5000, 'transactions': []},
            '5678': {'pin': '2222', 'balance': 3000, 'transactions': []}
        }
        self.current_user = None
        self.input_func = input_func if input_func else self.default_input
    
    def default_input(self, prompt):
        print(prompt)
        return "1234" if "card" in prompt.lower() else "1111"
    
    def authenticate_user(self):
        card_number = self.input_func("Enter your card number:")
        if card_number in self.users:
            pin = self.input_func("Enter your PIN:")
            if self.users[card_number]['pin'] == pin:
                self.current_user = card_number
                print("\nLogin successful!\n")
                return True
            else:
                print("Incorrect PIN.")
        else:
            print("Card number not found.")
        return False
    
    def check_balance(self):
        print(f"Your current balance is: ${self.users[self.current_user]['balance']}")
    
    def withdraw_cash(self):
        amount = float(self.input_func("Enter withdrawal amount: "))
        if 0 < amount <= self.users[self.current_user]['balance']:
            self.users[self.current_user]['balance'] -= amount
            self.users[self.current_user]['transactions'].append(f"Withdrew ${amount}")
            print(f"Success! You withdrew ${amount}. Remaining balance: ${self.users[self.current_user]['balance']}")
        else:
            print("Invalid amount or insufficient balance.")
    
    def deposit_cash(self):
        amount = float(self.input_func("Enter deposit amount: "))
        if amount > 0:
            self.users[self.current_user]['balance'] += amount
            self.users[self.current_user]['transactions'].append(f"Deposited ${amount}")
            print(f"Success! You deposited ${amount}. New balance: ${self.users[self.current_user]['balance']}")
        else:
            print("Invalid amount.")
    
    def show_transactions(self):
        print("\nTransaction History:")
        for transaction in self.users[self.current_user]['transactions']:
            print(transaction)
    
    def logout(self):
        print("Logging out...")
        self.current_user = None
    
    def run(self):
        if not self.authenticate_user():
            return
        
        while True:
            print("\n1. Check Balance\n2. Withdraw Cash\n3. Deposit Cash\n4. Transaction History\n5. Exit")
            choice = self.input_func("Choose an option: ")
            
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

if __name__ == "__main__":
    atm = ATM()
    atm.run()
