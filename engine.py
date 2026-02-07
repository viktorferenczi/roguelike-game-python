import random
import entities
import ui
import util

# TODO: need a proper character placement algorithm

def create_board(width, height):
    """
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    """
    board = []

    # Create empty board
    for _ in range(height):
        row = []
        for _ in range(width):
            cell = {
                "terrain": ui.FLOOR_ICON,
                "entity": None,
                "item": None}
            row.append(cell)
        board.append(row)

    # Add walls around the edges
    for col in range(width):
        board[0][col]["terrain"] = ui.WALL_ICON  # Top wall
        board[height - 1][col]["terrain"] = ui.WALL_ICON  # Bottom wall

    for row in range(height):
        board[row][0]["terrain"] = ui.WALL_ICON  # Left wall
        board[row][width - 1]["terrain"] = ui.WALL_ICON  # Right wall

    # Add gates
    start_position = (random.randint(1, height - 2), 0)
    end_position = (random.randint(1, height - 2), width - 1)
    add_gate(board, 'start', start_position)
    add_gate(board, 'end', end_position)

    items = ["item", "food", "hp_potion", "sword", "armor", "shield", "poison"]
    for item in items:
         item_position = (random.randint(1, height - 2), random.randint(1, width - 2))
         put_item_on_board(board, entities.create_item(item), item_position)

    put_player_on_board(board, entities.create_enemy())

    return board


def add_gate(board, gate_type, position):
    """
    Adds a gate to the board.

    Args:
    list: The game board
    str: The type of gate to add ('start' or 'end')

    Returns:
    Nothing
    """
    row, col = position
    if gate_type == 'start':
        board[row][col]["terrain"] = ui.START_GATE_ICON
    elif gate_type == 'end':
        board[row][col]["terrain"] = ui.END_GATE_ICON


def put_item_on_board(board, item, position):
    """
    Adds an item to the board at the specified position.

    Args:
    list: The game board
    dictionary: The item information containing the icon and coordinates
    tuple: The (row, col) position to place the item

    Returns:
    Nothing
    """
    row, col = position
    item['position'] = position
    board[row][col]["item"] = item


def remove_item_from_board(board, item):
    """
    Removes an item from the board.

    Args:
    list: The game board
    dictionary: The item information containing the icon and coordinates

    Returns:
    Nothing
    """
    row, col = item["position"]
    board[row][col]["item"] = None
    item["position"] = None


def pick_up_item(board, player):
    """
    Allows the player to pick up an item from the board if present at the player's position.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    """
    row, col = player["position"]
    cell = board[row][col]
   
    item = cell["item"]
    remove_item_from_board(board, item)
    if item.get("consumable") and item.get("auto_consume"):
        consume_item(player, item)
    else:
        item["position"] = 'inventory'
        player["inventory"].append(item)


def put_player_on_board(board, player):
    """
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    """
    row, col = player["position"]
    board[row][col]["entity"] = player


def remove_player_from_board(board, player):
    """
    Modifies the game board by removing the player icon from its previous coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    """
    row, col = player["position"]
    board[row][col]["entity"] = None
    player["position"] = None


def is_next_cell_enemy(board, new_row, new_col):
    """
    Checks if the next cell contains an enemy.

    Args:
    list: The game board
    int: The target row
    int: The target column

    Returns:
    bool: True if the next cell contains an enemy, False otherwise
    """
    cell = board[new_row][new_col]
    if cell["entity"] and cell["entity"]["type"] == "hostile":
        return True
    return False

def is_next_cell_item(board, new_row, new_col):
    """
    Checks if the next cell contains an item.

    Args:
    list: The game board
    int: The target row
    int: The target column

    Returns:
    bool: True if the next cell contains an item, False otherwise
    """
    cell = board[new_row][new_col]
    if cell["item"] is not None:
        return True
    return False

def attack(attacker, defender):
    """
    Handles the player attacking an enemy.

    Args:
    dictionary: The attacker information containing damage and coordinates
    dictionary: The defender information containing hp, defense and coordinates

    Returns:
    Nothing
    """
    damage_dealt = max(attacker["damage"] - defender.get("defense", 0), 0)
    defender["hp"] -= damage_dealt


def move_player(board, player, new_position):
    """
    Moves the player if the new position is valid.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates
    str: The input key

    Returns:
    Nothing
    """
    new_row, new_col = new_position

    if is_valid_move(board, new_row, new_col):
        remove_player_from_board(board, player)
        player["position"] = (new_row, new_col)


def is_occupied(board, row, col):
    """
    Checks if the specified position is occupied by an entity.

    Args:
    list: The game board
    int: The target row
    int: The target column

    Returns:
    bool: True if occupied, False otherwise
    """
    if board[row][col]["entity"] is not None:
        return True
    return False


def is_valid_move(board, row, col):
    """
    Checks if the move to the specified position is valid (within bounds and not a wall).

    Args:
    list: The game board
    int: The target row
    int: The target column

    Returns:
    bool: True if the move is valid, False otherwise
    """
    # Check bounds
    if is_out_of_bounds(board, row, col):
        return False

    if is_occupied(board, row, col):
        return False

    # Check for wall collision
    if board[row][col]["terrain"] == ui.WALL_ICON:
        return False

    return True


def is_out_of_bounds(board, row, col):
    """
    Checks if the specified position is out of the board bounds.

    Args:
    list: The game board
    int: The target row
    int: The target column

    Returns:
    bool: True if out of bounds, False otherwise
    """
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return True
    return False


def calculate_new_position(player, key):
    """
    Calculates the new position based on the input key.

    Args:
    dictionary: The player information containing the current position
    str: The input key (w, a, s, d)

    Returns:
    tuple: The new (row, col) position
    """
    row, col = player["position"]
    new_row, new_col = row, col

    if key == 'w':
        new_row -= 1
    elif key == 's':
        new_row += 1
    elif key == 'a':
        new_col -= 1
    elif key == 'd':
        new_col += 1

    return new_row, new_col


def get_gate_transition_delta(board, player, new_position):
    """
    Determines if the new position is a gate and returns the level transition delta.
    Args:
    list: The game board
    dictionary: The player information containing the current position
    tuple: The new (row, col) position

    Returns:
    int: 1 if moving to next level, -1 if moving to previous level, 0 otherwise
    """
    player_row, player_col = player["position"]
    player_new_row, player_new_col = new_position
    cell = board[player_row][player_col]
    on_gate = cell["terrain"] in (ui.START_GATE_ICON, ui.END_GATE_ICON)
    moving_out_of_bounds = is_out_of_bounds(board, player_new_row, player_new_col)

    if on_gate and moving_out_of_bounds:
        if board[player_row][player_col]["terrain"] == ui.END_GATE_ICON:
            return 1
        elif board[player_row][player_col]["terrain"] == ui.START_GATE_ICON:
            return -1
    return 0


def get_player_start_position(board, level_delta):
    """
    Gets the player's starting position based on level transition.

    Args:
    list: The game board
    int: The level transition delta

    Returns:
    tuple: The (row, col) starting position for the player
    """
    if level_delta == 1:  # Moving to next level
        for row_idx, row in enumerate(board):
            for col_idx, cell in enumerate(row):
                if cell["terrain"] == ui.START_GATE_ICON:
                    return row_idx, col_idx
    elif level_delta == -1:  # Moving to previous level
        for row_idx, row in enumerate(board):
            for col_idx, cell in enumerate(row):
                if cell["terrain"] == ui.END_GATE_ICON:
                    return row_idx, col_idx
    # Default start position (if no gate found)
    return 3, 3


def consume_item(player, item):
    """
    Consumes an item and applies its effects to the player.

    Args:
    dictionary: The player
    dictionary: The item

    Returns:
    Nothing
    """
    # Health restoration/poison
    if "heal" in item:
        player["hp"] = min(player["hp"] + item["heal"], player["max_hp"])

    # Damage increase
    if "damage" in item:
        player["damage"] += item["damage"]

    # Remove item from inventory
    try:
        player["inventory"].remove(item)
    except ValueError:
        pass  # Item wasn't in inventory


def equip_item(player, item):
    """
    Equips a weapon or armor to the player.

    Args:
    dictionary: The player
    dictionary: The item

    Returns:
    Nothing
    """
    item_equip_slot = item.get("equip_slot")
    unequip_item(player, item_equip_slot)
    item["position"] = item_equip_slot
    player[item_equip_slot] = item


def unequip_item(player, slot):
    """
    Unequips an item from the specified slot and returns it to the inventory.

    Args:
    dictionary: The player
    str: The slot to unequip ('weapon' or 'armor')

    Returns:
    Nothing
    """
    item = player.get(slot)
    if item:
        player[slot] = None
        item["position"] = 'inventory'
        player["inventory"].append(item)


def handle_inventory_item(player, item):
    """
    Handles inventory item actions based on item type.

    Args:
        player: Player object
        item: Item object

    Returns:
        bool: True if action was performed
    """

    if item.get("consumable"):
        consume_item(player, item)
        return True

    elif item.get("equippable"):
        equip_item(player, item)
        player["inventory"].remove(item)
        return True

    return False


def is_alive(player):
    """
    Checks if the player is alive.

    Args:
    dictionary: The player

    Returns:
    bool: True if alive, False if dead
    """
    return player["hp"] > 0


def is_near_player(player, enemy, distance=1):
    """
    Checks if the enemy is within a certain distance from the player.

    Args:
        player: The player object (dictionary)
        enemy: The enemy object (dictionary)
        distance: The distance threshold

    Returns:
        bool: True if enemy is within distance from player, False otherwise
    """

    player_row, player_col = player['position']
    enemy_row, enemy_col = enemy['position']
    return abs(player_row - enemy_row) <= distance and abs(player_col - enemy_col) <= distance



def move_enemy(board, enemy, player):
    """
    Move an enemy on the board autonomously.
    Enemy move randomly in one of the four directions, respecting walls.

    Args:
        player: The player object (dictionary)
        board: The game board (2D list)
        enemy: The enemy object (dictionary)
    """
    directions = [
        (-1, 0),  # up
        (1, 0),  # down
        (0, -1),  # left
        (0, 1)  # right
    ]

    if not is_alive(enemy):
        # print('not alive')
        # input()
        remove_player_from_board(board, enemy)
        return

    if is_near_player(player, enemy):
        attack(enemy, player)
    else:
        # Choose random direction
        dir_row, dir_col = random.choice(directions)
        current_row, current_col=enemy['position']
        new_row, new_col = current_row + dir_row, current_col + dir_col

        if is_valid_move(board, new_row, new_col):
            remove_player_from_board(board, enemy)
            enemy["position"] = (new_row, new_col)
            put_player_on_board(board, enemy)


def get_enemies(board):
    """
    Retrieves all enemy entities from the board.

    Args:
        board: The game board (2D list)
    Returns:
        list: A list of enemy entities (dictionaries)
    """
    enemies = []
    for row in board:
        for cell in row:
            if cell["entity"] and not cell["entity"]["type"] == "player":
                enemies.append(cell["entity"])
    return enemies

def request_race_choice(races):
    """
    Prompts the player to choose a race and validates the input.
    Args:
    races: A list of available races
    Returns:
    str: The chosen race
    """
    while True:
        race_choice = ui.request_input(f"\nChoice (1-{len(races)}): ")
        if race_choice in races:
            return race_choice
        ui.display_message("Invalid choice. Please try again.") 

def request_class_choice(classes):
    """
    Prompts the player to choose a class and validates the input.
    Args:
    classes: A list of available classes
    Returns:
    str: The chosen class
    """
    while True:
        class_choice = ui.request_input(f"\nChoice (1-{len(classes)}): ")
        if class_choice in classes:
            return class_choice
        ui.display_message("Invalid choice. Please try again.")


def handle_inventory(player):
    """
    Handles inventory interactions with item selection.

    Args:
    dict: The player object

    Returns:
    None
    """
    while True:
        inventory = player["inventory"]

        # Group items by name and add numbering as keys
        inventory_summary = {}
        for item in inventory:
            item_name = item["name"]
            if item_name in inventory_summary:
                inventory_summary[item_name]["quantity"] += 1
            else:
                inventory_summary[item_name] = {"item": item, "quantity": 1}

        grouped_inventory = {}
        for index, (item_name, item_info) in enumerate(inventory_summary.items(), start=1):
            grouped_inventory[str(index)] = item_info

        ui.clear_screen()
        ui.display_inventory(player, grouped_inventory)

        key = util.key_pressed()

        if key in ['q', 'i']:
            break

        if key.isdigit():
            item = grouped_inventory.get(key).get("item")
            if not item:
                ui.display_message("There is no item with that number.")
                ui.display_press_enter()
                continue
            elif handle_inventory_item(player, item):
                pass
            else:
                ui.display_message('Invalid action for that item.')
                ui.display_press_enter()
                pass

        if not is_alive(player):
            break

def create_player():
    """Character creation menu."""
    ui.clear_screen()
    ui.display_message("=== Character Creation ===\n")

    name = ui.request_input("Character name: ")

    races = {str(i): race for i, race in enumerate(entities.CHARACTERS_RACE_BONUS.keys(), start=1)}
    ui.display_race_choices(races)
    race_choice = request_race_choice(races)

    player_race = races.get(race_choice, "human")

    classes = {str(i): cls for i, cls in enumerate(entities.CHARACTERS_CLASS_BONUS.keys(), start=1)}

    ui.display_class_choices(classes)
    class_choice = request_class_choice(classes)

    player_class = classes.get(class_choice, "warrior")

    player = entities.create_player(name, player_race, player_class)

    return player



def run_level(board, player):
    """
    Runs a single level of the game.

    Args:
    list: Game board
    dict: Player object

    Returns:
    str: 'quit' if player quits,
    int: level delta if player goes through a gate
    """
    ui.clear_screen()

    while True:
        enemies = get_enemies(board)
        has_enemies = len(enemies) > 0

        if has_enemies:
            enemy = enemies[0]  # TODO: remove magic number

        if not is_alive(player):
            player["icon"] = ui.DEAD_PLAYER_ICON
            put_player_on_board(board, player)
            ui.display_board(board, player)
            ui.display_message("\nYou have died! Game Over.")
            raise SystemExit
        

        put_player_on_board(board, player)
        ui.display_board(board, player)

        key = util.key_pressed()

        if key == 'q':
            raise SystemExit

        elif key == 'i':
            handle_inventory(player)

        elif key in ['w', 'a', 's', 'd']:
            new_position = calculate_new_position(player, key)
            level_delta = get_gate_transition_delta(board, player, new_position)
            if level_delta == 0:

                new_row, new_col = new_position

                if is_next_cell_enemy(board, new_row, new_col):
                    enemy = board[new_row][new_col]["entity"]
                    attack(player, enemy)
                else:
                    move_player(board, player, new_position)

                if is_next_cell_item(board, new_row, new_col):
                    pick_up_item(board, player)

                if has_enemies:
                    move_enemy(board, enemy, player)
            else:
                remove_player_from_board(board, player)
                return level_delta

        ui.clear_screen()

