import ui

PLAYER_START_COL = 3
PLAYER_START_ROW = 3
ITEM_TYPES = {
    "item": {
        "icon": ui.ITEM_ICON,
        "name": "Item",
        "type": "item"
    },
    "food": {
        "icon": ui.FOOD_ICON,
        "name": "Food",
        "type": "food",
        "heal": 10,
        "auto_consume": True,
        "consumable": True,
    },
    "hp_potion": {
        "icon": ui.POTION_ICON,
        "name": "Healing Potion",
        "type": "potion",
        "heal": 30,
        "consumable": True,
    },
    "strength_potion": {
        "icon": ui.POTION_ICON,
        "name": "Strength Potion",
        "type": "potion",
        "damage": 5,
        "consumable": True,
    },
    "knife": {
        "icon": ui.KNIFE_ICON,
        "name": "Knife",
        "type": "weapon",
        "damage": 7,
        "equippable": True,
        "equip_slot": "weapon",
    },
    "sword": {
        "icon": ui.SWORD_ICON,
        "name": "Sword",
        "type": "weapon",
        "damage": 15,
        "equippable": True,
        "equip_slot": "weapon",
    },
    "shield": {
        "icon": ui.SHIELD_ICON,
        "name": "Shield",
        "type": "shield",
        "damage": 3,
        "defense": 5,
        "equippable": True,
        "equip_slot": "weapon",
    },
    "armor": {
        "icon": ui.ARMOR_ICON,
        "name": "Armor",
        "type": "armor",
        "defense": 5,
        "equippable": True,
        "equip_slot": "armor",
    },
    "shuriken": {
        "icon": ui.SHURIKEN_ICON,
        "name": "Shuriken",
        "type": "weapon",
        "damage": 5,
        "throwable": True,
    },
    "key": {
        "icon": ui.KEY_ICON,
        "name": "Key",
        "type": "key",
        "opens_doors": True,
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
        "race": "Human",
        "inventory": [],
        "hp": 10,
        "max_hp": 20,
        "damage": 5,
        "defense": 1,
        "experience": 0,
        "level": 1,
        "weapon": None,
        "armor": None
    }
    return player


def create_item(item_type="item", position=(5, 5)):
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
