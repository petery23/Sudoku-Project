import pygame

from engine.widget import Widget


class Box(Widget):
    size: tuple[int, int]
    color: pygame.Color

    def __init__(self, size: tuple[int, int] = (100, 100), color: pygame.Color = pygame.Color(0, 0, 0)):
        self.size = size
        self.color = color

    def get_size(self) -> tuple[int, int]:
        return self.size

    def draw_onto(self,
                  screen: pygame.Surface,
                  top_left: tuple[int, int] | None = None,
                  center: tuple[int, int] | None = None,
                  max_size: tuple[int, int] | None = None,
                  ) -> None:
        size = self.size if max_size is None else (min(max_size[0], self.size[0]), min(max_size[1], self.size[1]))

        rect = pygame.Rect(0, 0, 0, 0)
        if top_left is not None:
            rect.left = top_left[0]
            rect.right = size[0] + top_left[0]
            rect.bottom = size[1] + top_left[1]
            rect.top = top_left[1]
        elif center is not None:
            half_size = (size[0] / 2.0, size[1] / 2.0)
            rect.left = -half_size[0]
            rect.right = half_size[0]
            rect.bottom = -half_size[1]
            rect.top = half_size[1]
        else:
            assert top_left is not None or center is not None
            return

        pygame.draw.rect(screen, self.color, rect)