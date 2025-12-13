import os

PLAYER_ICON = '@'
WALL_ICON = '#'
FLOOR_ICON = ' '
START_GATE_ICON = 'S'
END_GATE_ICON = 'E'


def display_board(board):
    """
    Displays complete game board on the screen

    Args:
    list: The game board

    Returns:
    Nothing
    """
    for row in board:
        print(''.join(cell["entity"] if cell["entity"] is not None else cell["terrain"] for cell in row))


def clear_screen():
    """
    Clears the console screen
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
