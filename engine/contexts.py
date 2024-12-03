import pygame

from engine.input import InputState

class SceneChangeContext:
    input: InputState

    def __init__(self, input_state: InputState):
        self.input = input_state


class UpdateContext:
    dt: float
    screenSize: tuple[int, int]

    input: InputState

    def __init__(self, dt: float, screenSize: tuple[int, int], input_state: InputState):
        self.dt = dt
        self.screenSize = screenSize
        self.input = input_state


class RenderContext:
    surface: pygame.Surface

    def __init__(self, surface: pygame.Surface):
        self.surface = surface

