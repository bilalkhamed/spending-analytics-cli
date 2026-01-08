import questionary
import csv
import os
from src.config import CATEGORIES_FILE

# Define file name

def add_category():
    if not os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Description"])

    while True:
        print("\n--- New Category ---")
        
        name = questionary.text(
            "Enter category name:",
            validate=lambda text: False if text == "" else True
        ).ask()

        if name is None:
            print("Bye!")
            break
        
        description = questionary.text("Description (optional):").ask()

        # Save to CSV
        with open(CATEGORIES_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, description])

        questionary.print(f"✔ Saved: {name} with description '{description}'", style="bold fg:green")

        # Ask to continue
        if not questionary.confirm("Add another?").ask():
            break
