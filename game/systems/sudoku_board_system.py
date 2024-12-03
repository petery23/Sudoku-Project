import math

import pygame
from engine.contexts import SceneChangeContext
from engine.engine import UpdateContext, RenderContext
from engine.input import KeyboardEvent, KeyboardAction
from engine.system import System
from game.sudoku_board import SudokuBoard, SudokuBoardCell
from game.systems.highlight import ArrowKeyDirection
from game.widgets.sudoku_board_widget import SudokuBoardWidget
from engine.widgets.perspective_widget import PerspectiveWidget
from game.sudoku_board import SudokuBoard


class SudokuBoardSystem(System):
    board: SudokuBoard
    board_widget: PerspectiveWidget
    keyboard_inputs: list[int]

    def __init__(self, board: SudokuBoard, board_widget: PerspectiveWidget):
        self.board = board
        self.board_widget = board_widget
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

    def update(self, context: UpdateContext):
        board_changed = False

        while len(self.keyboard_inputs) > 0:
            new_value = self.keyboard_inputs.pop(0)
            if new_value == -1:
                # special new_value, enter was pressed
                continue

            if self.board.set_cell(self.board_widget.selected_cell, value=new_value, is_sketch=True):
                board_changed = True

        if board_changed:
            self.board.notify_change()

    def render(self, context: RenderContext):
        self.board_widget.x_rot = math.cos(context.time) * 10.0
        self.board_widget.y_rot = math.sin(context.time) * 10.0
        self.board_widget.draw_onto(context.surface, center=context.surface.get_rect().center)

    def exit_scope(self, context: SceneChangeContext):
        self.board.remove_observer(self.__on_board_state_changed)
        context.input.remove_observer(self.__on_keyboard_input)

    def dispose(self):
        pass

    def __on_board_state_changed(self, _):
        self.board_widget.repaint_board()