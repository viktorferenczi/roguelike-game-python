import random
import ui


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
            row.append({"terrain": ui.FLOOR_ICON, "entity": None, "item": None})
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

    # Add items randomly
    item_position = (random.randint(1, height - 2), random.randint(1, width - 2))
    put_item_on_board(board, {"icon": ui.ITEM_ICON}, item_position)

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
    board[row][col]["item"] = item["icon"]


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
    board[row][col]["entity"] = player["icon"]


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
    new_player_row, new_player_col = new_position
    cell = board[player_row][player_col]
    on_gate = cell["terrain"] in (ui.START_GATE_ICON, ui.END_GATE_ICON)
    moving_out_of_bounds = is_out_of_bounds(board, new_player_row, new_player_col)

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
