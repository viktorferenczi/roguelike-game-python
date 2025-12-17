import ui

PLAYER_START_COL = 3
PLAYER_START_ROW = 3
ITEM_TYPES = {
    "item": {
        "icon": ui.ITEM_ICON,
        "name": "Item",
    },
    "food": {
        "icon": ui.FOOD_ICON,
        "name": "Food",
        "heal": 10,
    },
    "potion": {
        "icon": ui.POTION_ICON,
        "name": "Potion",
        "heal": 30,
    },
    "sword": {
        "icon": ui.SWORD_ICON,
        "name": "Sword",
        "damage": 15,
    },
    "shield": {
        "icon": ui.SHIELD_ICON,
        "name": "Shield",
        "defense": 10,
    }
}


def create_player():
    """
    Creates a 'player' dictionary for storing all player related information - i.e. player icon, player position.

    Returns:
    dictionary
    """
    player = {
        "icon": ui.PLAYER_ICON,
        "position": (PLAYER_START_ROW, PLAYER_START_COL),
        "name": "Player",
        "inventory": []
    }
    return player


def create_item(item_type="item", position=(5,5)):
    """
    Creates an item dictionary for storing item related information - i.e. item icon, item position.
    Item types can be 'item', 'food', 'potion', 'sword', 'shield'.

    Args:
    item_type: str
    position: tuple

    Returns:
    dictionary
    """
    base = ITEM_TYPES[item_type]

    item = {
        "icon": ui.ITEM_ICON,
        "position": position,
        "name": "Item"
    }

    item.update(base)
    return item



