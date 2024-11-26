import pygame

from engine.input import InputState


class UpdateContext:
    dt: float
    input: InputState

    def __init__(self, dt: float):
        self.dt = dt


class RenderContext:
    surface: pygame.Surface

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
