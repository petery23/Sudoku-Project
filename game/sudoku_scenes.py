from typing import Callable

import pygame

from engine.systems.button_system import ButtonSystem
from engine.systems.draw_system import DrawSystem
from engine.widgets.box import Box
from engine.widgets.button import Button
from engine.widgets.outlined_box import OutlinedBox
from engine.widgets.perspective_widget import PerspectiveWidget
from engine.widgets.positioned import Positioned
from engine.widgets.text import Text
from game.scenes.game_scene import GameScene
from game.scenes.main_menu_scene import MainMenuScene
from game.sudoku_board import SudokuBoard, SudokuBoardCell
from game.sudoku_difficulty import SudokuDifficulty
from game.systems.highlight_system import HighlightSystem
from game.systems.sudoku_board_system import SudokuBoardSystem
from game.widgets.sudoku_board_widget import SudokuBoardWidget

WHITE = pygame.Color(255, 255, 255)
PURPLE = pygame.Color(128, 0, 128)

USE_PERSPECTIVE_EFFECT = False


def get_main_menu_scene(width: int, height: int, on_difficulty_selected: Callable[[SudokuDifficulty], None]) -> MainMenuScene:
    welcome_font = pygame.font.Font(None, 80)
    gm_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 48)

    return MainMenuScene([
        DrawSystem([
            Positioned(
                position=(width // 2, height // 4),
                child=Text("Welcome to Sudoku!", WHITE, welcome_font)
            ),
            Positioned(
                position=(width // 2, height // 3),
                child=Text("Select Game Mode:", WHITE, gm_font)
            ),
        ]),
        ButtonSystem([
            Button(
                position=(width // 2 - 300, int(height / 1.5)),
                on_interact=lambda: on_difficulty_selected(SudokuDifficulty.EASY),
                foreground=Text("Easy", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
            Button(
                position=(width // 2, int(height / 1.5)),
                on_interact=lambda: on_difficulty_selected(SudokuDifficulty.MEDIUM),
                foreground=Text("Medium", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
            Button(
                position=(width // 2 + 300, int(height / 1.5)),
                on_interact=lambda: on_difficulty_selected(SudokuDifficulty.HARD),
                foreground=Text("Hard", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
        ]),
    ])


def on_reset_button(board_widget, board):
    for x in range(board.get_size()[0]):
        for y in range(board.get_size()[1]):
            if not board.get_cell((y, x)).is_given():
                board.get_cell((y,x)).set_value(0)

    board_widget.board = board
    board.notify_change()

def get_game_scene(width: int, height: int, board: SudokuBoard,
                   on_restart_button, on_exit_button: Callable) -> GameScene:
    button_font = pygame.font.Font(None, 48)
    ui_size = min(width, height) - (0 if USE_PERSPECTIVE_EFFECT else 9 * 9)

    board_widget = SudokuBoardWidget(
                board=board,
                ui_size=(ui_size, ui_size),
            )

    board_pixel_size = board_widget.get_size()
    board_cell_pixel_size = (board_pixel_size[0] // board.get_size()[0], board_pixel_size[1] // board.get_size()[1])

    selection_outline_widget = Positioned(
                    position=(0, 0),
                    child=OutlinedBox(
                        size=board_cell_pixel_size,
                        width=4,
                        color=pygame.Color(128, 0, 128),
                    ),
                )

    return GameScene((width, height), [
        ButtonSystem([
            Button(
                position = (width - 175, height - 220),
                on_interact = lambda: on_reset_button(board_widget, board),
                foreground = Text("Reset", WHITE, button_font),
                background = Box((120, 50), color = PURPLE),
                size = (120, 50)
            ),
            Button(
                position = (width - 175, height - 160),
                on_interact = lambda: on_restart_button(),
                foreground = Text("Restart", WHITE, button_font),
                background = Box((120, 50), color = PURPLE),
                size = (120, 50)
            ),
            Button(
                position = (width - 175, height - 100),
                on_interact = lambda: on_exit_button(),
                foreground = Text("Exit", WHITE, button_font),
                background = Box((120, 50), color = PURPLE),
                size = (120, 50)
            ),
        ]),
        SudokuBoardSystem(
            board=board_widget.board,
            board_widget=board_widget,
            perspective_widget=PerspectiveWidget(
                enable_mipmaps=True,
                size=board_widget.get_size(),
                child=board_widget,
            ) if USE_PERSPECTIVE_EFFECT else None,
        ),
        HighlightSystem(
            board=board_widget.board,
            board_widget=board_widget,
            selection_outline_widget=selection_outline_widget,
            perspective_widget = PerspectiveWidget(
                enable_mipmaps=False,
                size=board_widget.get_size(),
                child=selection_outline_widget
            ) if USE_PERSPECTIVE_EFFECT else None,
        ),
    ])

def get_end_screen(width: int, height: int, isWinner: bool, on_restart_button: Callable): 
    welcome_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 48)

    if isWinner:
        return MainMenuScene([
            DrawSystem([
                Positioned(
                    position=(width // 2, height // 4),
                    child=Text("You win!", WHITE, welcome_font)
                ),
            ]),
            ButtonSystem([
                Button(
                    position=(width // 2, int(height / 1.5)),
                    on_interact=lambda: on_restart_button(),
                    foreground=Text("Medium", WHITE, button_font),
                    background=Box((250, 50), color=PURPLE),
                    size=(250, 50)
                ),
            ]),
    ])
    else:
        return MainMenuScene([
            DrawSystem([
                Positioned(
                    position=(width // 2, height // 4),
                    child=Text("You lose!", WHITE, welcome_font)
                ),
            ]),
            ButtonSystem([
                Button(
                    position=(width // 2, int(height / 1.5)),
                    on_interact=lambda: on_restart_button(),
                    foreground=Text("Medium", WHITE, button_font),
                    background=Box((250, 50), color=PURPLE),
                    size=(250, 50)
                ),
            ]),
    ])

