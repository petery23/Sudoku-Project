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
        # match context.input.mouse_state:
        #     case MouseState.DOWN:
        #         self.buttons_pressed = []
        #         for button in self.buttons:
        #             if not button.interactable: continue
        #             if not button.rect.collidepoint(context.input.mouse_down_pos): continue
        #             self.buttons_pressed.append(button)
        #     case MouseState.DRAGGING:
        #         for i in range(len(self.buttons_pressed) - 1, -1, -1):
        #             button = self.buttons_pressed[i]
        #             if not button.interactable:
        #                 self.buttons_pressed.pop(i)
        #                 continue
        #             if not button.rect.collidepoint(context.input.mouse_pos):
        #                 self.buttons_pressed.pop(i)
        #                 continue
        #     case MouseState.UP:
        #         for button in self.buttons_pressed:
        #             if not button.interactable: continue
        #             if not button.rect.collidepoint(context.input.mouse_up_pos): continue
        #             button.on_interact()
        pass


    def render(self, context: RenderContext):
        self.board_widget.draw_onto(context.surface, center=context.surface.get_rect().center)

    def exit_scope(self):
        self.board.remove_observer(self.__on_board_state_changed)

    def dispose(self):
        pass

    def __on_board_state_changed(self, _):
        pass