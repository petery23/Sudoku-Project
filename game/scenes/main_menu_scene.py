import pygame, random

from engine.contexts import UpdateContext, RenderContext
from engine.scene import Scene
from engine.system import System


BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)


class MainMenuScene(Scene):
    def __init__(self, systems: list[System]) -> None:
        self.lines: list[list[float]] = []

        super().__init__(systems)


    def enter_scope(self) -> None:
        self.lines = [[random.uniform(0.0, 1.0), random.uniform(-1.0, 1.0)] for _ in range(50)]

        super().enter_scope()


    def update(self, context: UpdateContext) -> None:
        for line in self.lines:
            line[1] += 0.5 * context.dt
            if line[1] > 1.0:
                line[1] = random.uniform(-0.5, 0)

        super().update(context)


    def render(self, context: RenderContext) -> None:
        context.surface.fill(BLACK)

        width = context.surface.get_width()
        height = context.surface.get_height()

        for line in self.lines:
            start = (line[0] * width, line[1] * height)
            end = (line[0] * width, line[1] * height + 50)
            pygame.draw.line(context.surface, PURPLE, start, end, 2)

        super().render(context)


    def exit_scope(self) -> None:
        super().exit_scope()

    def dispose(self) -> None:
        super().dispose()