import questionary
import pandas as pd
from src.utils import get_most_spent_categry
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from datetime import datetime


DATA_FILE = 'data/expenses.csv'

df = pd.read_csv(DATA_FILE)

def average_expense():
    console = Console()
    mean = df['Amount'].mean()
    # console.print(f"[bold green]✔ Average Expense: {mean:.2f} JOD[/bold green]")

    console.print(Align.left(Panel(f"[bold green]{mean:.2f} JOD[/bold green]", border_style="blue", title="Average Expense")))

    categories = df.groupby('Category')['Amount'].mean()

    table = Table(title='Average expense by category')
    table.add_column('Category', style='cyan', no_wrap=True)
    table.add_column('Average Amount', style='magenta')
    for category, amount in categories.items():
        table.add_row(category, f"{amount:.2f} JOD")
    
    console.print(table)


def average_by_day():
    pd.set_option('mode.copy_on_write', True)
    console = Console()
    df_day = df.groupby('Date')['Amount'].sum().reset_index()

    df_day['Weekday'] = pd.to_datetime(df_day['Date']).dt.day_name()

    weekday_top_3 = df_day.groupby('Weekday')['Amount'].mean().reset_index().sort_values(by='Amount', ascending=False).head(3)
    

    median = df_day['Amount'].median()
    console.print(Align.left(Panel(f"[bold green]{median:.2f} JOD[/bold green]", border_style="blue", title="Average Expense")))

    days_above_avg = df_day.loc[df_day['Amount'] > median]
    
    days_above_avg['Category'] = days_above_avg['Date'].apply(lambda date: get_most_spent_categry(df, date))

    table = Table(title='Top 3 weekdays with highest average expenses')
    table.add_column('Weekday', style='cyan', no_wrap=True)
    table.add_column('Average Amount', style='magenta')
    for row in weekday_top_3.itertuples():
        table.add_row(row.Weekday, f"{row.Amount:.2f} JOD")
    console.print(table)

    table = Table(title=f'Days with expenses above average {days_above_avg.shape[0]} / {df_day.shape[0]}')
    table.add_column('Date', style='cyan', no_wrap=True)
    table.add_column('Total Amount', style='magenta')
    table.add_column('Most spent on', style='yellow', no_wrap=False)
    for row in days_above_avg.itertuples():
        table.add_row(datetime.strptime(row.Date, "%Y-%m-%d").strftime("%b %d, %a"), f"{row.Amount:.2f} JOD", row.Category, end_section=True)
    console.print(table)

    CV = df_day['Amount'].std() / df_day['Amount'].mean()
    
    if CV < 0.25:
        text = '[bold green]✔ Your daily expenses are consistent! Keep it up[/bold green]'
    elif CV < 0.5:
        text = '[bold yellow]⚠ Your daily expenses show moderate variability. Try to monitor your spending more closely.[/bold yellow]'
    else:
        text = '[bold red]✘ Your daily expenses are highly variable. Consider creating a budget to manage your spending better.[/bold red]'

    console.print(Align.left(Panel(text, border_style="blue", title="Expense Variability", subtitle=f"Coefficient of Variation: {CV:.2f}")))


def predict_rest_of_month():
    print("Predicting expenses for the rest of the month...")

operations = {
    'Average Expense': average_expense,
    'Average by Day': average_by_day,
    'Predict Rest of Month': predict_rest_of_month
}

def main():
    operation = questionary.select(
            "Select an option:",
            choices=operations.keys()
        ).ask()
    
    operations[operation]()
