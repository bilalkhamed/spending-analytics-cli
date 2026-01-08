import matplotlib.pyplot as plt
import seaborn as sns
from src.config import EXPENSES_FILE
import pandas as pd

def generate_charts():
    df = pd.read_csv(EXPENSES_FILE)
    df['Date'] = pd.to_datetime(df['Date'])

    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # Chart 1: Daily Spending
    daily = df.groupby('Date')['Amount'].sum().reset_index()
    sns.lineplot(data=daily, x='Date', y='Amount', ax=axs[0], marker='o', color='tab:blue')
    axs[0].set_title("Daily Spending Trend")
    axs[0].axhline(daily['Amount'].mean(), color='r', linestyle='--', label='Average')
    axs[0].grid(True, linestyle='--', alpha=0.6)

    # Chart 2: Category Breakdown
    cat_sum = df.groupby('Category')['Amount'].sum().reset_index().sort_values('Amount', ascending=False)
    sns.barplot(data=cat_sum, x='Amount', y='Category', ax=axs[1], palette='viridis', hue='Amount')
    axs[1].set_title("Spending by Category")

    # Save and Open
    plt.tight_layout()
    plt.show()
