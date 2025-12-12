import random


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
            row.append({"terrain": " ", "entity": None})
        board.append(row)

    # Add walls around the edges
    for col in range(width):
        board[0][col]["terrain"] = "#"  # Top wall
        board[height - 1][col]["terrain"] = "#"  # Bottom wall

    for row in range(height):
        board[row][0]["terrain"] = "#"  # Left wall
        board[row][width - 1]["terrain"] = "#"  # Right wall

    # Add gates
    board[random.randint(1, height - 2)][0]["terrain"] = "G"  # Start gate
    board[random.randint(1, height - 2)][width - 1]["terrain"] = "G"  # End gate

    return board


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
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        return False

    # Check for wall collision
    if board[row][col]["terrain"] == "#":
        return False

    return True


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