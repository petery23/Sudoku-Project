import pygame

from engine.input import InputState


class UpdateContext:
    dt: float
    screenSize: tuple[int, int]

    input: InputState

    def __init__(self, dt: float, screenSize: tuple[int, int]):
        self.dt = dt
        self.screenSize = screenSize


class RenderContext:
    surface: pygame.Surface

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
