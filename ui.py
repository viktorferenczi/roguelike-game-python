import os

PLAYER_ICON = 'ฏ'
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
DEAD_PLAYER_ICON = '✝'


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


def clear_screen():
    """
    Clears the console screen
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
