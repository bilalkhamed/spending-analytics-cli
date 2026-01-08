# Spending Analytics CLI

A Python-based personal finance tool that combines data entry with some data analysis insights.

## Features

- Add expenses / purchases with `questionary` for validated data-entry.

- Add custom categories to categorize your expenses

- View all expenses and see how much of your monthly budget is used

- View expenses by category, and see some related stats like most spent, most frequent purchases, etc.

- View expenses by date

- Analysis: `Average by day`, which calculates summary statistics such as the median daily spend, standard deviation, and coefficient of variation (CV) to measure spending consistency

- User settings, which currently only allows you to change the default currency or your monthly budget.

## Tech Stack

- Core: `Python` 3.13.5
- Data analysis: `pandas`
- Terminal UI/UX: `rich` and `questionary`
- Visualization: `matplotlib` and `seaborn`

## Setup and Usaege

1. Clone the repo

```bash
git clone https://github.com/bilalkhamed/spending-analytics-cli.git
cd spending-analytics-cli
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python main.py
```

## Future plan:

Utilize a linear regression model to predict spending for the remaining days of the month.
