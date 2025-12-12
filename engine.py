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
            row.append(" ")
        board.append(row)

    # Add walls around the edges
    for col in range(width):
        board[0][col] = "#"  # Top wall
        board[height - 1][col] = "#"  # Bottom wall

    for row in range(height):
        board[row][0] = "#"  # Left wall
        board[row][width - 1] = "#"  # Right wall

    # Add gates
    board[random.randint(1, height - 2)][0] = "G"  # Start gate
    board[random.randint(1, height - 2)][width - 1] = "G"  # End gate

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
    board[row][col] = player["icon"]
