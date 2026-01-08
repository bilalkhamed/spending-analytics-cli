import questionary
from src import categories, expenses, analysis, utils, charts

operations = ['Add Category', 'Add Expense', 'View All Expenses', 'View By Category', 'View By Date' , 'Exit']

operations = {
    'Add Category': categories.add_category,
    'Add Expense': expenses.add_expense,
    'View All Expenses': expenses.view_expenses,
    'View By Category': expenses.view_by_category,
    'View By Date': lambda: expenses.view_by_date(utils.date_input()),
    'View Analysis': analysis.main,
    'View Charts': charts.generate_charts,
    'Exit': lambda: print("Exiting the program.")
}

def main():
    while True:
        operation = questionary.select(
            "Select an operation:",
            choices=operations.keys()
        ).ask()

        if operation == 'Exit':
            operations[operation]()
            break
        else:
            operations[operation]()

      
        
if __name__ == "__main__":
    main()