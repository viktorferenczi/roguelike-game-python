def create_board(width, height):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''
    # The engine.create_board function returns an empty, rectangular board as a list of lists of the given size, containing characters according to the field type (e.g. spaces all around and wall icons on its edges).
    # The game has at least 3 boards/levels with different inhabitants.
    # Gates are added on the edges (one gate character instead of one piece of wall).
    board = []
    for i in range(width):
        row = []
        for j in range(height):
            if i == 0 or i == width - 1 or j == 0 or j == height - 1:
                row.append('#')  # Wall character
            else:
                row.append(' ')  # Empty space
        board.append(row)
    # Adding gates (for simplicity, placing one gate on each side)
    board[0][height // 2] = 'G'  # Top gate
    board[width - 1][height // 2] = 'G'  # Bottom gate
    board[width // 2][0] = 'G'  # Left gate
    board[width // 2][height - 1] = 'G'  # Right gate
    return board


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    pass
