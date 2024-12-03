from engine.engine import Engine
from game.sudoku_board import SudokuBoard
from game.sudoku_difficulty import SudokuDifficulty
from game.sudoku_scenes import get_main_menu_scene, get_game_scene
from sudoku_generator import generate_sudoku

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    engine = Engine("Sudoku", (WINDOW_WIDTH, WINDOW_HEIGHT))


    def on_difficulty_selected(difficulty: SudokuDifficulty):
        # Start game

        board_state, solution = generate_sudoku(9, difficulty.value)
        board = SudokuBoard(board_state, solution)


        game_scene = get_game_scene(WINDOW_WIDTH, WINDOW_HEIGHT, board)
        engine.load_scene(game_scene)


    main_menu_scene = get_main_menu_scene(WINDOW_WIDTH, WINDOW_HEIGHT, on_difficulty_selected)
    engine.load_scene(main_menu_scene)

    engine.main_loop()
    engine.dispose()


if __name__ == "__main__":
    main()

