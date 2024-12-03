import pygame

from engine.input import InputState

class SceneChangeContext:
    input: InputState

    def __init__(self, input_state: InputState):
        self.input = input_state


class UpdateContext:
    time: float
    dt: float
    screenSize: tuple[int, int]

    input: InputState

    def __init__(self, time: float, dt: float, screenSize: tuple[int, int], input_state: InputState):
        self.time = time
        self.dt = dt
        self.screenSize = screenSize
        self.input = input_state


class RenderContext:
    time: float
    surface: pygame.Surface

    def __init__(self, time: float, surface: pygame.Surface):
        self.time = time
        self.surface = surface

