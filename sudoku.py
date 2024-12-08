from engine.engine import Engine
from game.sudoku_board import SudokuBoard
from game.sudoku_difficulty import SudokuDifficulty
from game.sudoku_scenes import get_main_menu_scene, get_game_scene, get_end_screen
from sudoku_generator import generate_sudoku

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    engine = Engine("Sudoku", (WINDOW_WIDTH, WINDOW_HEIGHT))

    def on_restart_button():
        main_menu_scene = get_main_menu_scene(WINDOW_WIDTH, WINDOW_HEIGHT, on_difficulty_selected, on_exit_button)
        engine.load_scene(main_menu_scene)

    def on_exit_button():
        engine.dispose()
        exit()

    def on_game_over(is_winner: bool):
        end_screen = get_end_screen(WINDOW_WIDTH, WINDOW_HEIGHT, is_winner, on_restart_button)
        engine.load_scene(end_screen)

    def on_difficulty_selected(difficulty: SudokuDifficulty):
        # Start game

        board_state, solution = generate_sudoku(9, difficulty.value)
        board = SudokuBoard(board_state, solution, difficulty)

        for x in range(board.get_size()[0]):
            for y in range(board.get_size()[1]):
                if not (board.get_cell((x, y)).get_value()[0] == 0):
                    board.get_cell((x, y)).__given = True

        game_scene = get_game_scene(WINDOW_WIDTH, WINDOW_HEIGHT, board,
                                    on_restart_button,
                                    on_game_over)
        engine.load_scene(game_scene)

    main_menu_scene = get_main_menu_scene(WINDOW_WIDTH, WINDOW_HEIGHT, on_difficulty_selected, on_exit_button)
    engine.load_scene(main_menu_scene)

    engine.main_loop()
    engine.dispose()


if __name__ == "__main__":
    main()

