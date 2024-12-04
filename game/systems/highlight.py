from enum import Enum

import pygame

from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.input import KeyboardEvent, KeyboardAction
from engine.system import System
from engine.widgets.perspective_widget import PerspectiveWidget
from game.sudoku_board import SudokuBoard
from game.widgets.sudoku_board_widget import SudokuBoardWidget

HIGHLIGHT_PURPLE = (128,0,128)
HIGHLIGHT_WIDTH = 4

class ArrowKeyDirection(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class HighlightSystem(System):
    board_cell_pixel_size: tuple[int, int]
    board_pixel_size: tuple[int, int]

    perspective_widget: PerspectiveWidget
    board_widget: SudokuBoardWidget

    arrow_key_inputs: list[ArrowKeyDirection]

    def __init__(self, board: SudokuBoard, board_widget: SudokuBoardWidget, perspective_widget: PerspectiveWidget):
        self.perspective_widget = perspective_widget
        self.board_widget = board_widget
        
        self.board_pixel_size = self.board_widget.get_size()
        self.board_cell_pixel_size = (self.board_pixel_size[0] // board.get_size()[0], self.board_pixel_size[1] // board.get_size()[1])

        self.arrow_key_inputs = []

    def __on_keyboard_input(self, event: KeyboardEvent):
        if event.action != KeyboardAction.DOWN: return
        match event.key:
            case pygame.K_UP:
                self.arrow_key_inputs.append(ArrowKeyDirection.UP)
            case pygame.K_DOWN:
                self.arrow_key_inputs.append(ArrowKeyDirection.DOWN)
            case pygame.K_RIGHT:
                self.arrow_key_inputs.append(ArrowKeyDirection.RIGHT)
            case pygame.K_LEFT:
                self.arrow_key_inputs.append(ArrowKeyDirection.LEFT)

    def enter_scope(self, context: SceneChangeContext):
        context.input.add_observer(self.__on_keyboard_input)

        super().enter_scope(context)

    def update(self, context: UpdateContext):
        if abs(context.input.mouse_delta[0]) + abs(context.input.mouse_delta[1]) >= 1:
            # mouse has moved
            # finds cell being hovered over
            top_left_x = (context.screenSize[0] - self.board_pixel_size[0]) // 2
            top_left_y = (context.screenSize[1] - self.board_pixel_size[1]) // 2

            mouse_x, mouse_y = context.input.mouse_pos

            if mouse_x < top_left_x or mouse_x > top_left_x + self.board_pixel_size[0]:
                # mouse is outside board horizontally
                pass
            elif mouse_y < top_left_y or mouse_y > top_left_y + self.board_pixel_size[1]:
                # mouse is outside board vertically
                pass
            else:
                self.board_widget.selected_cell = ((mouse_x - top_left_x) // self.board_cell_pixel_size[0],
                                                   (mouse_y - top_left_y) // self.board_cell_pixel_size[1])

        else:
            # mouse hasn't moved, defer to arrow keys
            while len(self.arrow_key_inputs) > 0:
                input_direction = self.arrow_key_inputs.pop(0)
                match input_direction:
                    case ArrowKeyDirection.UP:
                        self.board_widget.selected_cell = (self.board_widget.selected_cell[0], max(self.board_widget.selected_cell[1] - 1, 0))
                    case ArrowKeyDirection.DOWN:
                        self.board_widget.selected_cell = (self.board_widget.selected_cell[0], min(self.board_widget.selected_cell[1] + 1, self.board_widget.board.get_size()[1] - 1))
                    case ArrowKeyDirection.RIGHT:
                        self.board_widget.selected_cell = (min(self.board_widget.selected_cell[0] + 1, self.board_widget.board.get_size()[0] - 1), self.board_widget.selected_cell[1])
                    case ArrowKeyDirection.LEFT:
                        self.board_widget.selected_cell = (max(self.board_widget.selected_cell[0] - 1, 0), self.board_widget.selected_cell[1])

        super().update(context)

    def render(self, context: RenderContext):
        # board is centered
        # context.surface.get_size() gives pixel size of entire screen
        # context.surface.get_size()
        # draws outline around hovered cell

        top_left_x = (context.surface.get_size()[0] - self.board_pixel_size[0]) // 2
        top_left_y = (context.surface.get_size()[1] - self.board_pixel_size[1]) // 2

        hovered_x = top_left_x + self.board_widget.selected_cell[0] * self.board_cell_pixel_size[0]
        hovered_y = top_left_y + self.board_widget.selected_cell[1] * self.board_cell_pixel_size[1]

        pygame.draw.lines(context.surface,
                          HIGHLIGHT_PURPLE,
                          True,
                          [
                            (hovered_x,                                 hovered_y), 
                            (hovered_x + self.board_cell_pixel_size[0], hovered_y),
                            (hovered_x + self.board_cell_pixel_size[0], hovered_y + self.board_cell_pixel_size[1]), 
                            (hovered_x,                                 hovered_y + self.board_cell_pixel_size[1])],
                          HIGHLIGHT_WIDTH)

        super().render(context)

    def exit_scope(self, context: SceneChangeContext):
        context.input.remove_observer(self.__on_keyboard_input)

        super().exit_scope(context)

    def dispose(self):
        super().dispose()