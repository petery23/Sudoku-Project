import pygame, random

from engine.contexts import UpdateContext, RenderContext
from engine.scene import Scene
from engine.system import System


BLACK = (0, 0, 0)


class GameScene(Scene):
    background: pygame.Surface

    def __init__(self, window_size: tuple[int, int], systems: list[System]) -> None:
        super().__init__(systems)
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, window_size)


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
            pygame.draw.line(context.surface, (128,0,128), start, end, 2)

        super().render(context)


    def exit_scope(self) -> None:
        super().exit_scope()

    def dispose(self) -> None:
        super().dispose()