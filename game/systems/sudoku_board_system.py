from engine.engine import UpdateContext, RenderContext
from engine.input import MouseState
from engine.system import System
from game.sudoku_board import SudokuBoard
from game.widgets.sudoku_board_widget import SudokuBoardWidget


class SudokuBoardSystem(System):
    board: SudokuBoard
    board_widget: SudokuBoardWidget

    def __init__(self, board_widget: SudokuBoardWidget):
        self.board = board_widget.board
        self.board_widget = board_widget



    def enter_scope(self):
        self.board.add_observer(self.__on_board_state_changed)

    def update(self, context: UpdateContext):
        pass

    def render(self, context: RenderContext):
        self.board_widget.draw_onto(context.surface, center=context.surface.get_rect().center)

    def exit_scope(self):
        self.board.remove_observer(self.__on_board_state_changed)

    def dispose(self):
        pass

    def __on_board_state_changed(self, _):
        pass