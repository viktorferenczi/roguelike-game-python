import os

ENTITY_ICON = '@'
PLAYER_ICON = 'ฏ'
DEAD_PLAYER_ICON = '✝'
FRIENDLY_NPC_ICON = 'ซ'
ENEMY_NPC_ICON = 'ภ'
NEUTRAL_NPC_ICON = '๕'

WALL_ICON = '▒'
FLOOR_ICON = ' '
START_GATE_ICON = 'Ω'
END_GATE_ICON = 'Ώ'

ITEM_ICON = 'i'
FOOD_ICON = '≡'
POTION_ICON = 'δ'
POISON_ICON = '☠'
SWORD_ICON = '!'
SHIELD_ICON = 'Θ'
ARMOR_ICON = '◊'
KEY_ICON = '๛'
SHURIKEN_ICON = '✦'
KNIFE_ICON = '/'


def display_board(board, player):
    """
    Displays complete game board on the screen

    Args:
    list: The game board
    dict: The player object

    Returns:
    None
    """
    if player:
        print(f"HP: {player['hp']}/{player['max_hp']} | "
              f"Damage: {player['damage']} | "
              f"Defense: {player['defense']}")
        print("-" * 40)

    cell_display = []

    for row in board:
        for cell in row:
            if cell["entity"] is not None:
                cell_display.append(cell["entity"]['icon'])
            elif cell["item"] is not None:
                cell_display.append(cell["item"]['icon'])
            else:
                cell_display.append(cell["terrain"])
        cell_display.append('\n')
    print(''.join(cell_display))


def display_inventory(player, grouped_inventory):
    """
    Displays the player's inventory with stacked items.
    Args:
    dict: The player object
    dict: A dictionary where each key is a string number (for selection)
    and the value is a dictionary with:
        - "item": the item dictionary
        - "quantity": the number of that item in the inventory
    Returns:
    None
    """
    # Header
    print("=" * 40)
    print(f"HP: {player['hp']}/{player['max_hp']}")
    weapon = player.get("weapon") or {"name": "", "icon": ""}
    print(f"Weapon: {weapon.get('name', '')} ({weapon.get('icon', '')})")
    armor = player.get("armor") or {"name": "", "icon": ""}
    print(f"Armor: {armor.get('name', '')} ({armor.get('icon', '')})")
    print("=" * 40)
    print("\nInventory:")

    # Inventory items
    if not player["inventory"]:
        print("  (empty)")
    else:
        for choice, item_info in grouped_inventory.items():
            item = item_info["item"]
            quantity = item_info["quantity"]
            print(f"  {choice}. {item['name']} x{quantity} ({item['icon']})")

    print("=" * 40)

def display_press_enter():
    """
    Displays a message prompting the user to press Enter to continue.

    Returns:
    None
    """
    input("\nPress Enter to continue...")

def display_message(message):
    """
    Displays a message to the user.

    Args:
    str: The message to display

    Returns:
    None
    """
    print(message)

def request_input(prompt):
    """
    Requests input from the user with a given prompt.

    Args:
    str: The prompt to display

    Returns:
    str: The user's input
    """
    return input(prompt)

def clear_screen():
    """
    Clears the console screen
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def display_race_choices(races):
    """
    Displays the available race choices to the user.    
    Args:
    dict: A dictionary where each key is a string number (for selection)
    and the value is the name of the race   
    Returns:
    None
    """
    display_message("\nChoose your race:")
    for key, race in races.items():
        display_message(f"{key}. {race.capitalize()}")

def display_class_choices(classes):
    """
    Displays the available class choices to the user.    
    Args:
    dict: A dictionary where each key is a string number (for selection)
    and the value is the name of the class   
    Returns:
    None
    """
    display_message("\nChoose your class:")
    for key, cls in classes.items():
        display_message(f"{key}. {cls.capitalize()}")
