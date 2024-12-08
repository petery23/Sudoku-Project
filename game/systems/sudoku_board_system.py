from typing import Callable

import pygame
from engine.contexts import SceneChangeContext
from engine.engine import UpdateContext, RenderContext
from engine.input import KeyboardEvent, KeyboardAction
from engine.system import System
from engine.widgets.perspective_widget import PerspectiveWidget
from game.sudoku_board import SudokuBoard
from game.widgets.sudoku_board_widget import SudokuBoardWidget


class SudokuBoardSystem(System):
    board: SudokuBoard
    board_widget: SudokuBoardWidget
    perspective_widget: PerspectiveWidget | None
    keyboard_inputs: list[int]

    on_game_over: Callable[[bool], None]

    def __init__(self, board: SudokuBoard, board_widget: SudokuBoardWidget, perspective_widget: PerspectiveWidget | None,
                 on_game_over: Callable[[bool], None]):
        self.board = board
        self.board_widget = board_widget
        self.perspective_widget = perspective_widget
        self.keyboard_inputs = []

        self.on_game_over = on_game_over

    def enter_scope(self, context: SceneChangeContext):
        self.board.add_observer(self.__on_board_state_changed)
        context.input.add_observer(self.__on_keyboard_input)

    def __on_keyboard_input(self, event: KeyboardEvent):
        if event.action != KeyboardAction.DOWN: return
        match event.key:
            case pygame.K_1:
                self.keyboard_inputs.append(1)
            case pygame.K_2:
                self.keyboard_inputs.append(2)
            case pygame.K_3:
                self.keyboard_inputs.append(3)
            case pygame.K_4:
                self.keyboard_inputs.append(4)
            case pygame.K_5:
                self.keyboard_inputs.append(5)
            case pygame.K_6:
                self.keyboard_inputs.append(6)
            case pygame.K_7:
                self.keyboard_inputs.append(7)
            case pygame.K_8:
                self.keyboard_inputs.append(8)
            case pygame.K_9:
                self.keyboard_inputs.append(9)
            case pygame.K_RETURN | pygame.K_SPACE:
                self.keyboard_inputs.append(-1)
            case pygame.K_BACKSPACE | pygame.K_DELETE:
                self.keyboard_inputs.append(-2)

    def update(self, context: UpdateContext):
        board_changed = False

        while len(self.keyboard_inputs) > 0:
            new_value = self.keyboard_inputs.pop(0)
            if new_value == -1:
                # commiting the current sketched value
                display_value, is_empty, is_sketch = self.board.get_cell(self.board_widget.selected_cell).get_value()
                if not is_empty and is_sketch and self.board.get_cell(self.board_widget.selected_cell).set_value(value=display_value, is_sketch=False):
                    board_changed = True

            elif new_value == -2:
                # Backspace key was pressed, clear the cell
                if self.board.get_cell(self.board_widget.selected_cell).set_value(value=0, clear = True):
                    board_changed = True

            else:
                # sketch the value
                if self.board.get_cell(self.board_widget.selected_cell).set_value(value=new_value, is_sketch=True):
                    board_changed = True

        if board_changed:
            self.board.notify_change()

            if self.board.is_full():
                if self.board.is_solved():
                    self.on_game_over(True)
                else:
                    self.on_game_over(False)



    def render(self, context: RenderContext):
        if self.perspective_widget is not None:
            self.perspective_widget.x_rot = context.x_rot
            self.perspective_widget.y_rot = context.y_rot
            self.perspective_widget.draw_onto(context.surface, center=context.surface.get_rect().center)
        else:
            self.board_widget.draw_onto(context.surface, center=context.surface.get_rect().center)

    def exit_scope(self, context: SceneChangeContext):
        self.board.remove_observer(self.__on_board_state_changed)
        context.input.remove_observer(self.__on_keyboard_input)

    def dispose(self):
        pass

    def __on_board_state_changed(self, _):
        self.board_widget.repaint_board()