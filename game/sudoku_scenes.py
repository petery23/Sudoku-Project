from typing import Callable

import pygame

from engine.systems.button_system import ButtonSystem
from engine.systems.draw_system import DrawSystem
from engine.widgets.box import Box
from engine.widgets.button import Button
from engine.widgets.positioned import Positioned
from engine.widgets.text import Text
from game.scenes.game_scene import GameScene
from game.scenes.main_menu_scene import MainMenuScene
from game.sudoku_board import SudokuBoard
from game.sudoku_difficulty import SudokuDifficulty
from game.systems.sudoku_board_system import SudokuBoardSystem
from game.widgets.sudoku_board_widget import SudokuBoardWidget

WHITE = pygame.Color(255, 255, 255)
PURPLE = pygame.Color(128, 0, 128)


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


def get_game_scene(width: int, height: int, board: SudokuBoard) -> GameScene:
    ui_size = min(width, height) - 45

    return GameScene((width, height), [
        SudokuBoardSystem(
            board_widget=SudokuBoardWidget(
                board=board,
                ui_size=(ui_size, ui_size),
            ),
        ),
    ])
