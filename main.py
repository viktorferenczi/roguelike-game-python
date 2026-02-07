import engine

BOARD_WIDTH = 30
BOARD_HEIGHT = 20

def main():
    player = engine.create_player()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    board2 = engine.create_board(BOARD_WIDTH+10, BOARD_HEIGHT)
    boards = [board, board2]
    level = 0

    while True:
        level_delta = engine.run_level(boards[level], player)

        level += level_delta

        if level < 0:  # TODO: need other implementation for going below level 0 (gate could have id for connected level, and connected gate/cell)
            level = 0
            player["position"] = engine.get_player_start_position(boards[level], 1)
        elif level >= len(boards):
            break
        else:
            player["position"] = engine.get_player_start_position(boards[level], level_delta)


if __name__ == '__main__':
    main()
