import pygame

from engine.widget import Widget


class Text(Widget):
    surface: pygame.Surface

    def __init__(self, text: str, color: pygame.color.Color, font: pygame.font.Font):
        self.surface = font.render(text, True, color)

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