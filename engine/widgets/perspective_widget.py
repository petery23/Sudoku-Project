import glm
import pygame
import pygame_shaders

from engine.widget import Widget, PositionedWidget
from game.scenes.game_scene import PERSPECTIVE_FOV

PERSPECTIVE_VERTEX_SHADER_PATH = "shaders/perspective.vert"
PERSPECTIVE_FRAGMENT_SHADER_PATH = "shaders/perspective.frag"


class PerspectiveWidget(Widget):
    surface: pygame.Surface
    child: PositionedWidget
    shader: pygame_shaders.Shader

    x_rot: float = 0.0
    y_rot: float = 0.0

    mouse_pos: tuple[int, int] = (0, 0)

    def __init__(self, child: PositionedWidget, size: tuple[int, int], enable_mipmaps: bool = False):
        self.child = child
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self.shader = pygame_shaders.Shader(
            PERSPECTIVE_VERTEX_SHADER_PATH,
            PERSPECTIVE_FRAGMENT_SHADER_PATH,
            target_surface=self.surface,
            enable_mipmaps=enable_mipmaps)


    def get_size(self) -> tuple[int, int]:
        return self.surface.get_size()


    def __repaint_child(self) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.child.draw_positioned(self.surface)
        #print(f"Perspective ({self}): repainted")


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

        should_repaint_child = self.child.parent_should_repaint()
        if should_repaint_child:
            self.__repaint_child()

        proj_mat = glm.perspective(glm.radians(PERSPECTIVE_FOV), 1, 0.1, 100.0)
        view_mat = glm.lookAt((0.0, 0.0, 2.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        model_mat = glm.lookAt((0.0, 0.0, 0.0), (self.x_rot, self.y_rot, -2.0), (0.0, 1.0, 0.0))

        self.shader.send("u_projMat", [x for xs in proj_mat.to_list() for x in xs])
        self.shader.send("u_viewMat", [x for xs in view_mat.to_list() for x in xs])
        self.shader.send("u_modelMat", [x for xs in model_mat.to_list() for x in xs])

        render = self.shader.render(update_surface=should_repaint_child)

        dest.blit(render, target)
