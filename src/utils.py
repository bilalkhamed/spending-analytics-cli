import pandas as pd
from datetime import datetime

import questionary

def load_categories(csv_file):
    """Load categories from a CSV file and return as a list."""
    try:
        df = pd.read_csv(csv_file)
        if 'Name' in df.columns:
            return df['Name'].dropna().tolist()
        else:
            raise ValueError("CSV file must contain 'Name' column.")
    except FileNotFoundError:
        with open(csv_file, 'w') as f:
            f.write("Name,Description\n")  # Create an empty CSV with header
        return []
    except ValueError:
        raise ValueError("Error reading categories from CSV file.")

def date_input():
    def validate_date(text):
            if text == '':
                return True
            try:
                datetime.strptime(text, '%Y-%m-%d')
                return True
            except ValueError:
                return 'Please enter a valid date in YYYY-MM-DD format'
    date_str = questionary.text(
            'Enter Date (YYYY-MM-DD) [leave empty for today]:',
            validate=validate_date
        ).ask()
        
    if not date_str:
            date_str = datetime.today().strftime('%Y-%m-%d')

    return datetime.strptime(date_str, '%Y-%m-%d').date()

def get_most_spent_categry(df: pd.DataFrame, date: str):
    day = df.loc[df['Date'] == date]
    grp = day.groupby('Category')['Amount'].sum().reset_index()
    return grp.loc[grp['Amount'].idxmax(axis=0)]['Category']
