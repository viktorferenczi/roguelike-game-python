import os

PLAYER_ICON = '@'
WALL_ICON = '#'
FLOOR_ICON = ' '
START_GATE_ICON = 'S'
END_GATE_ICON = 'E'
ITEM_ICON = '!'
FOOD_ICON = '%'
POTION_ICON = '+'
SWORD_ICON = '/'
SHIELD_ICON = ']'


def display_board(board):
    """
    Displays complete game board on the screen

    Args:
    list: The game board

    Returns:
    None
    """
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


def clear_screen():
    """
    Clears the console screen
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
