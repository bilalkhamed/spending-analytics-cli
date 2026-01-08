import questionary
from src import categories, expenses, utils

# Define file name
DATA_FILE = 'data/categories.csv'

operations = ['Add Category', 'Add Expense', 'View All Expenses', 'View By Category', 'View By Date' , 'Exit']


def main():
    while True:
        operation = questionary.select(
            "Select an operation:",
            choices=operations
        ).ask()

        if operation == 'Add Category':
            categories.add_category()
        elif operation == 'Add Expense':
            expenses.add_expense()
        elif operation == 'View All Expenses':
            expenses.view_expenses()
        elif operation == 'View By Category':
            expenses.view_by_category()
        elif operation == 'View By Date':
            date = utils.date_input()
            expenses.view_by_date(date)
        elif operation == 'Exit':
            print("Exiting the program.")
            break
        
if __name__ == "__main__":
    main()