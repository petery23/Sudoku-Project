import pygame

from engine.widget import Widget


class OutlinedBox(Widget):
    surface: pygame.Surface

    def __init__(self, size: tuple[int, int] = (100, 100), width: int = 2, color: pygame.Color = pygame.Color(0, 0, 0)):
        self.surface = pygame.Surface((size[0] + width * 2, size[1] + width * 2), flags=pygame.SRCALPHA)
        pygame.draw.lines(self.surface, color, True,[(width,   width),
                                                     (size[0] + width, width),
                                                     (size[0] + width, size[1] + width),
                                                     (width,   size[1] + width),
                                                     ], width)

    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()

    def draw_onto(self,
                  dest: pygame.Surface,
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

        dest.blit(self.surface, target)