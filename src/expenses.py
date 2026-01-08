import questionary
import csv
from datetime import datetime
import os
from src.utils import load_categories, date_input
import pandas as pd
from rich.console import Console
from rich.table import Table 
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress
from src.config import EXPENSES_FILE, CATEGORIES_FILE, USER_CONFIG


categories = load_categories(CATEGORIES_FILE)

CURRENCY = USER_CONFIG['currency']

def add_expense():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Amount', 'Category', 'Description'])
    while True:
        print('\n--- New Transaction ---')
        
        amount = questionary.text(
            f'Enter amount ({CURRENCY}):',
            validate=lambda text: True if text.replace('.', '', 1).isdigit() and float(text) > 0 else 'Please enter a valid positive number'
        ).ask()

        if amount is None:
            print('Bye!')
            break
        
        category = questionary.select(
            'Select Category:',
            choices=categories
        ).ask()

        if category is None:
            print('Bye!')
            break
        
        # 3. Get Date (Default to today)
        date = date_input()

        # 4. Optional Notes
        notes = questionary.text('Description (optional):').ask()

        # Save to CSV
        with open(EXPENSES_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, amount, category, notes])

        questionary.print(f'✔ Saved: {amount} {CURRENCY} for {category} on {date}', style='bold fg:green')

        # Ask to continue
        if not questionary.confirm('Add another?').ask():
            break

def view_expenses():
    if not os.path.exists(EXPENSES_FILE):
        print('No expenses recorded yet.')
        return

    df = pd.read_csv(EXPENSES_FILE)
    if df.empty:
        print('No expenses recorded yet.')
        return
    
    df = df.sort_values(by='Date', ascending=False)
    
    table = Table(title='Expenses')    

    table.add_column('Date', justify='center', style='cyan', no_wrap=True)
    table.add_column('Amount', justify='right', style='green')
    table.add_column('Category', justify='left', style='magenta')
    table.add_column('Description', justify='left', style='yellow')

    for row in df.itertuples():
        table.add_row(
            row.Date,
            f'{row.Amount:.2f} {CURRENCY}',
            row.Category,
            str(row.Description) if pd.notna(row.Description) else '-'
        )
    
    console = Console()
    console.print(table)

    total = df['Amount'].sum()
    percent = (total / USER_CONFIG['monthly_budget']) * 100
    console.print(f'Total Spent: {total:.2f} {CURRENCY}')
    console.print(f'{percent:.2f}% used of your monthly budget of {USER_CONFIG["monthly_budget"]} {CURRENCY}')

def view_by_category():
    if not os.path.exists(EXPENSES_FILE):
        print('No expenses recorded yet.')
        return

    df = pd.read_csv(EXPENSES_FILE)
    console = Console()

    # Group by 'Category' and sum the 'Amount'
    # This turns raw rows into meaningful data
    summary = df.groupby('Category')['Amount'].sum().reset_index()
    
    # Sort by highest spend first
    summary = summary.sort_values(by='Amount', ascending=False)

    total_spent = summary['Amount'].sum()
    most_frequent_cat = df['Category'].mode()[0]
    highest_expense = summary.loc[summary['Amount'].idxmax()]
    
    # --- PART 2: Create "Cards" for the Stats ---
    # We use Panels to make them look like cards
    stats_cards = [
        Panel(f"[green]{total_spent:.2f} {CURRENCY}[/green]", title="Total Spent", ),
        Panel(f"[cyan]{most_frequent_cat}[/cyan]", title="Most Purchases", ),
        Panel(f"[red]{highest_expense['Amount']:.2f} {CURRENCY}[/red]\n({highest_expense['Category']})", title="Most Spent", )
    ]

    # Print the cards centered
    console.print("\n")
    console.print(Align.left(Columns(stats_cards)))
    console.print("\n")

    # Print it using your nice Table method...
    table = Table(title='Expenses by Category')
    table.add_column('Category', justify='left', style='magenta')
    table.add_column(f'Total Amount ({CURRENCY})', justify='right', style='green')
    for row in summary.itertuples():
        table.add_row(
            row.Category,
            f'{row.Amount:.2f} {CURRENCY}',
        )


    table.add_section()
    table.add_row(
        'Total',
        f'{summary["Amount"].sum():.2f} {CURRENCY}',
    )

    console.print(table)


def view_by_date(date):
    if not os.path.exists(EXPENSES_FILE):
        print('No expenses recorded yet.')
        return

    df = pd.read_csv(EXPENSES_FILE)
    console = Console()

    expenses = df.loc[df['Date'] == datetime.strftime(date, '%Y-%m-%d')]

    if expenses.empty:
        console.print(f'No expenses found for [bold]{datetime.strftime(date, "%Y-%m-%d")}[/bold].', style='yellow')
        return

    table = Table(title=f'{date} expenses')

    table.add_column('Amount', justify='right', style='green')
    table.add_column('Category', justify='left', style='magenta')
    table.add_column('Description', justify='left', style='yellow')

    for row in expenses.itertuples():
        table.add_row(
            f'{row.Amount:.2f} {CURRENCY}',
            row.Category,
            str(row.Description) if pd.notna(row.Description) else '-'
        )
    
    table.add_section()

    table.add_row(
        f'Total: [bold]{expenses["Amount"].sum():.2f} {CURRENCY}[/bold]',
        '',
        f''
    )

    console.print(table)