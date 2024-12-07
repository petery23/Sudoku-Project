import math

import pygame
from engine.contexts import SceneChangeContext
from engine.engine import UpdateContext, RenderContext
from engine.input import KeyboardEvent, KeyboardAction
from engine.system import System
from engine.widgets.perspective_widget import PerspectiveWidget
from game.sudoku_board import SudokuBoard
from game.widgets.sudoku_board_widget import SudokuBoardWidget


PERSPECTIVE_ROT_ANGLE = 60.0


class SudokuBoardSystem(System):
    board: SudokuBoard
    board_widget: SudokuBoardWidget
    perspective_widget: PerspectiveWidget | None
    keyboard_inputs: list[int]

    def __init__(self, board: SudokuBoard, board_widget: SudokuBoardWidget, perspective_widget: PerspectiveWidget | None):
        self.board = board
        self.board_widget = board_widget
        self.perspective_widget = perspective_widget
        self.keyboard_inputs = []

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
            case pygame.K_RETURN:
                self.keyboard_inputs.append(-1)
            case pygame.K_BACKSPACE:
                self.keyboard_inputs.append(-2)

    def update(self, context: UpdateContext):
        board_changed = False

        while len(self.keyboard_inputs) > 0:
            new_value = self.keyboard_inputs.pop(0)
            if new_value == -1:
                # commiting the current sketched value
                cell = self.board.get_cell(self.board_widget.selected_cell)
                sketched_value = cell.get_value()[0] if cell.get_value()[2] else 0
                if sketched_value != 0 and self.board.set_cell(self.board_widget.selected_cell, value=sketched_value, is_sketch=False):
                    board_changed = True

            elif new_value == -2:
                # Backspace key was pressed, clear the cell
                if self.board.set_cell(self.board_widget.selected_cell, value=0, clear = True):
                    board_changed = True

            else:
                # sketch the value
                if self.board.set_cell(self.board_widget.selected_cell, value=new_value, is_sketch=True):
                    board_changed = True

        if board_changed:
            self.board.notify_change()

            if self.board.is_full():
                if self.board.is_solved():
                    # end game: win
                    pass
                else:
                    # end game: lose
                    pass



    def render(self, context: RenderContext):
        if self.perspective_widget is not None:
            self.perspective_widget.x_rot = math.cos(context.time) * PERSPECTIVE_ROT_ANGLE
            self.perspective_widget.y_rot = math.sin(context.time) * PERSPECTIVE_ROT_ANGLE
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