import json
from datetime import datetime


transactions = {}


def load_transactions():
    global transactions
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = {}

def save_transactions():
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)

def read_bulk_transactions_from_file(filename):
    global transactions
    try:
        with open(filename, 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format in file.")


def add_transaction():
    global transactions
    try:
        category = input("Enter the category: ")
        amount = float(input("Enter the amount: "))
        date_added = input("Enter date (YYYY-MM-DD): ")
        transaction_type = input("Enter type (Income/Expense): ").capitalize()

        datetime.strptime(date_added, '%Y-%m-%d')

        if category in transactions:
            transactions[category].append({"amount": amount, "date": date_added, "type": transaction_type})
        else:
            transactions[category] = [{"amount": amount, "date": date_added, "type": transaction_type}]

        save_transactions()
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number for amount.")
    except KeyError:
        print("Invalid input. Please enter a valid type of expense.")
    except Exception as e:
        print(f"Error: {e}")

def view_transactions():
    global transactions
    if not transactions:
        print("No transactions available.")
    else:
        for category, expenses in transactions.items():
             print(f"{category}:")
             for expense in expenses:
                print(f"  Amount: {expense['amount']}, Date: {expense['date']}, Type: {expense['type']}")


def update_transaction():
    global transactions
    try:
        view_transactions()
        category = input("Enter the category to update: ")
        index = int(input("Enter 0: "))
        
        if category in transactions and 0 <= index < len(transactions[category]):
            amount = float(input("Enter the new amount: "))
            date_added = input("Enter the new date (YYYY-MM-DD): ")
            transaction_type = input("Enter the new type (Income/Expense): ").capitalize()

            datetime.strptime(date_added, '%Y-%m-%d')

            transactions[category][index] = {"amount": amount, "date": date_added, "type": transaction_type}
            save_transactions()
            print("Transaction updated successfully.")
        else:
            print("Invalid category or index.")

    except ValueError:
        print("Invalid input. Please enter a valid number for amount and a valid integer for index.")
    except Exception as e:
        print(f"Error: {e}")


def delete_transaction():
    global transactions
    try:
        view_transactions()
        category = input("Enter the category to delete from: ")
        index = int(input("Enter 0: "))
        if 0 <= index < len(transactions.get(category, [])):
            del transactions[category][index]
            if not transactions[category]:
                del transactions[category]
            save_transactions()
            print("Transaction deleted successfully.")
        else:
            print("Invalid index or category.")
    except ValueError:
        print("Invalid input. Please enter valid data.")
    except Exception as e:
        print(f"Error: {e}")

def display_summary():
    global transactions
    total_expense = sum(expense['amount'] for expenses in transactions.values() for expense in expenses if expense['type'] == 'Expense')
    total_income = sum(expense['amount'] for expenses in transactions.values() for expense in expenses if expense['type'] == 'Income')
    print(f"Total Expenses: {total_expense}")
    print(f"Total Income: {total_income}")
    print(f"Net Income: {total_income - total_expense}")

def main_menu():
    load_transactions()
    while True:
        print("\n==== Personal Finance Tracker ====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            save_transactions()
            print("Thank you for using the Personal Finance Tracker.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main_menu()
