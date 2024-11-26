import pygame, random

from engine.engine import Engine
from engine.systems.button_system import ButtonSystem
from engine.systems.draw_system import DrawSystem
from engine.widgets.box import Box
from engine.widgets.button import Button
from engine.widgets.positioned import Positioned
from engine.widgets.text import Text
from game.scenes.main_menu import MainMenuScene


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    engine = Engine("Sudoku", (WINDOW_WIDTH, WINDOW_HEIGHT))

    WHITE = pygame.Color(255, 255, 255)
    PURPLE = pygame.Color(128, 0, 128)

    welcome_font = pygame.font.Font(None, 80)
    gm_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 48)

    scene = MainMenuScene([
        DrawSystem([
            Positioned(
                position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4),
                child=Text("Welcome to Sudoku!", WHITE, welcome_font)
            ),
            Positioned(
                position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3),
                child=Text("Select Game Mode:", WHITE, gm_font)
            ),
        ]),
        ButtonSystem([
            Button(
                position=(WINDOW_WIDTH // 2 - 300, int(WINDOW_HEIGHT / 1.5)),
                on_interact=lambda: print("Easy button pressed!"),
                foreground=Text("Easy", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
            Button(
                position=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT / 1.5)),
                on_interact=lambda: print("Medium button pressed!"),
                foreground=Text("Medium", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
            Button(
                position=(WINDOW_WIDTH // 2 + 300, int(WINDOW_HEIGHT / 1.5)),
                on_interact=lambda: print("Hard button pressed!"),
                foreground=Text("Hard", WHITE, button_font),
                background=Box((250, 50), color=PURPLE),
                size=(250, 50)
            ),
        ]),
    ])
    engine.load_scene(scene)

    engine.main_loop()
    engine.dispose()


if __name__ == "__main__":
    main()

