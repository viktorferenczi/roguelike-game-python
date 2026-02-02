import util
import engine
import ui
import entities

BOARD_WIDTH = 30
BOARD_HEIGHT = 20


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
    # enemies = []
    # enemies.append(entities.create_enemy())
    enemy = entities.create_enemy()

    while True:
        if not engine.is_alive(player):
            player["icon"] = ui.DEAD_PLAYER_ICON
            engine.put_player_on_board(board, player)
            ui.display_board(board, player)
            print("\nYou have died! Game Over.")
            return 'quit'

        engine.put_player_on_board(board, player)
        engine.put_player_on_board(board, enemy)
        ui.display_board(board, player)

        key = util.key_pressed()

        if key == 'q':
            return 'quit'

        elif key == 'i':
            handle_inventory(player)

        elif key in ['w', 'a', 's', 'd']:
            new_position = engine.calculate_new_position(player, key)
            level_delta = engine.get_gate_transition_delta(board, player, new_position)
            if level_delta == 0:
                engine.move_player(board, player, new_position)
                engine.pick_up_item(board, player)
                engine.move_enemy(board, enemy, player)
            else:
                engine.remove_player_from_board(board, player)
                return level_delta

        ui.clear_screen()


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
                print("There is no item with that number.")
                input("\nPress Enter to continue...")
                continue
            elif engine.handle_inventory_item(player, item):
                # input("\nPress Enter to continue...")
                pass
            else:
                print('Invalid action for that item.')
                input("\nPress Enter to continue...")
                pass

        if not engine.is_alive(player):
            break


def create_player():
    """Character creation menu."""
    ui.clear_screen()
    print("=== Character Creation ===\n")

    name = input("Character name: ")

    races = {str(i): race for i, race in enumerate(entities.CHARACTERS_RACE_BONUS.keys(), start=1)}

    print("\nChoose your race:")
    for key, race in races.items():
        print(f"{key}. {race.capitalize()}")
    race_choice = input(f"\nChoice (1-{len(races)}): ")

    player_race = races.get(race_choice, "human")

    classes = {str(i): cls for i, cls in enumerate(entities.CHARACTERS_CLASS_BONUS.keys(), start=1)}

    print("\nChoose your class:")
    for key, cls in classes.items():
        print(f"{key}. {cls.capitalize()}")
    class_choice = input(f"\nChoice (1-{len(classes)}): ")

    player_class = classes.get(class_choice, "warrior")

    player = entities.create_player(name, player_race, player_class)

    return player


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

        if level < 0:  # TODO: need other implementation for going below level 0 (gate could have id for connected level, and connected gate/cell)
            level = 0
            player["position"] = engine.get_player_start_position(boards[level], 1)
        elif level >= len(boards):
            break
        else:
            player["position"] = engine.get_player_start_position(boards[level], level_delta)


if __name__ == '__main__':
    main()
