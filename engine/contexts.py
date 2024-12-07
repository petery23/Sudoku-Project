import pygame

from engine.input import InputState

class SceneChangeContext:
    input: InputState

    def __init__(self, input_state: InputState):
        self.input = input_state


class UpdateContext:
    time: float
    dt: float
    screen_size: tuple[int, int]

    input: InputState

    def __init__(self, time: float, dt: float, screen_size: tuple[int, int], input_state: InputState):
        self.x_rot = 0.0
        self.y_rot = 0.0

        self.time = time
        self.dt = dt
        self.screen_size = screen_size
        self.input = input_state


class RenderContext:
    time: float
    surface: pygame.Surface

    def __init__(self, time: float, surface: pygame.Surface):
        self.x_rot = 0.0
        self.y_rot = 0.0

        self.time = time
        self.surface = surface

