from rich.console import Console
from src.config import USER_CONFIG, USER_CONFIG_FILE
import questionary
import json

def settings():
  
  while True:
      choices = []
      for key, value in USER_CONFIG.items():
          choices.append(f"{key}: {value}")
      
      choices.append("Back")

      selection = questionary.select(
          'Settings Menu',
          choices=choices
      ).ask()

      if selection == "Back":
          break

      selected_key = selection.split(":")[0]
      
      change_setting(selected_key)

def change_setting(key):
    console = Console()
    current_value = USER_CONFIG[key]
    
    # 1. DETERMINE TYPE (Int, Float, or String?)
    if isinstance(current_value, int):
        prompt_type = int
        validate_func = lambda x: x.isdigit()
    elif isinstance(current_value, float):
        prompt_type = float
        validate_func = lambda x: x.replace('.', '', 1).isdigit()
    else:
        prompt_type = str
        validate_func = lambda x: True

    # 2. ASK FOR INPUT (With Validation)
    new_value_str = questionary.text(
        f"Enter new value for '{key}' (Current: {current_value}):",
        validate=validate_func
    ).ask()

    if new_value_str is None: return # User cancelled

    # 3. CONVERT TYPE
    new_value = prompt_type(new_value_str)

    # 4. UPDATE MEMORY
    USER_CONFIG[key] = new_value

    # 5. UPDATE FILE (Safe Write)
    # We write the WHOLE dictionary to ensure consistency
    with open(USER_CONFIG_FILE, 'w') as f:
        json.dump(USER_CONFIG, f, indent=4)

    console.print(f"[bold green]✔ Updated {key} to {new_value}[/bold green]")