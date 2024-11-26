from typing import Callable

import pygame
from pygame import Surface

from engine.widget import Widget, PositionedWidget


class Button(PositionedWidget):
    on_click: Callable[[], None]
    surface: Surface
    rect: pygame.Rect
    interactable: bool

    def __init__(self,
                 position: tuple[int, int],
                 on_click: Callable[[], None],
                 foreground: Widget,
                 background: Widget,
                 size: tuple[float, float]):
        super().__init__(position)

        self.on_click = on_click
        self.surface = Surface(size)
        self.surface.fill("RED")
        self.rect = self.surface.get_rect(center=self.position)
        background.draw_onto(self.surface, center=self.rect.center)
        foreground.draw_onto(self.surface, center=self.rect.center)

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def draw_onto(self,
                  screen: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        if top_left is not None:
            target = top_left
        elif center is not None:
            target = self.surface.get_rect(center=center)
        else:
            assert top_left is not None or center is not None
            return

        screen.blit(self.surface, target)

    def draw_positioned(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, self.rect)

