import util
import engine
import ui

PLAYER_START_COL = 3
PLAYER_START_ROW = 3

BOARD_WIDTH = 30
BOARD_HEIGHT = 20


def create_player():
    """
    Creates a 'player' dictionary for storing all player related information - i.e. player icon, player position.

    Returns:
    dictionary
    """
    player = {
        "icon": ui.PLAYER_ICON,
        "position": (PLAYER_START_ROW, PLAYER_START_COL)
    }
    return player


def run_level(board, player):
    """
    Runs a single level of the game.

    Args:
    list: Game board
    dict: Player object
    int: Current level

    Returns:
    str: 'quit' if player quits,
    int: level delta if player goes through a gate
    """
    ui.clear_screen()

    while True:
        engine.put_player_on_board(board, player)
        ui.display_board(board)

        key = util.key_pressed()
        if key == 'q':
            return 'quit'
        elif key in ['w', 'a', 's', 'd']:
            new_position = engine.calculate_new_position(player, key)
            level_delta = engine.get_gate_transition_delta(board, player, new_position)
            if level_delta == 0:
                engine.move_player(board, player, new_position)
            else:
                engine.remove_player_from_board(board, player)
                return level_delta

        ui.clear_screen()


def main():
    player = create_player()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    board2 = engine.create_board(40, 20)
    boards = [board, board2]
    level = 0

    while True:
        level_delta = run_level(boards[level], player)

        if level_delta == 'quit':  # TODO: need other way to quit
            break

        level += level_delta

        if level < 0:
            level = 0
        elif level >= len(boards):
            break

        player["position"] = engine.get_player_start_position(boards[level], level_delta)


if __name__ == '__main__':
    main()
