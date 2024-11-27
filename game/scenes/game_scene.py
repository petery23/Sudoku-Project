import pygame

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
        super().enter_scope()


    def update(self, context: UpdateContext) -> None:
        super().update(context)


    def render(self, context: RenderContext) -> None:
        context.surface.blit(self.background, (0, 0))

        super().render(context)


    def exit_scope(self) -> None:
        super().exit_scope()

    def dispose(self) -> None:
        super().dispose()