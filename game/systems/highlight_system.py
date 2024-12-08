from enum import Enum

import glm
import pygame

from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.input import KeyboardEvent, KeyboardAction, MouseState
from engine.system import System
from engine.widgets.perspective_widget import PerspectiveWidget
from engine.widgets.positioned import Positioned
from game.scenes.game_scene import PERSPECTIVE_FOV
from game.sudoku_board import SudokuBoard
from game.widgets.sudoku_board_widget import SudokuBoardWidget

class ArrowKeyDirection(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class HighlightSystem(System):
    board_cell_pixel_size: tuple[int, int]
    board_pixel_size: tuple[int, int]

    board_widget: SudokuBoardWidget
    positioned_widget: Positioned
    perspective_widget: PerspectiveWidget | None

    arrow_key_inputs: list[ArrowKeyDirection]

    hover_mode: bool = False

    def __init__(self, board: SudokuBoard, board_widget: SudokuBoardWidget, selection_outline_widget: Positioned, perspective_widget: PerspectiveWidget | None):
        self.perspective_widget = perspective_widget
        self.positioned_widget = selection_outline_widget
        self.board_widget = board_widget
        
        self.board_pixel_size = self.board_widget.get_size()
        self.board_cell_pixel_size = (self.board_pixel_size[0] // board.get_size()[0], self.board_pixel_size[1] // board.get_size()[1])

        self.arrow_key_inputs = []

    def __on_keyboard_input(self, event: KeyboardEvent):
        if event.action != KeyboardAction.DOWN: return
        match event.key:
            case pygame.K_UP:
                self.arrow_key_inputs.append(ArrowKeyDirection.UP)
            case pygame.K_DOWN:
                self.arrow_key_inputs.append(ArrowKeyDirection.DOWN)
            case pygame.K_RIGHT:
                self.arrow_key_inputs.append(ArrowKeyDirection.RIGHT)
            case pygame.K_LEFT:
                self.arrow_key_inputs.append(ArrowKeyDirection.LEFT)
            case pygame.K_h:
                self.hover_mode = not self.hover_mode

    def enter_scope(self, context: SceneChangeContext):
        context.input.add_observer(self.__on_keyboard_input)


    def update(self, context: UpdateContext):
        previous = self.board_widget.selected_cell

        input_condition = abs(context.input.mouse_delta[0]) + abs(context.input.mouse_delta[1]) >= 1 if self.hover_mode else context.input.mouse_state == MouseState.DOWN
        if input_condition:
            proj_mat = glm.perspective(glm.radians(PERSPECTIVE_FOV), 1, 0.1, 100.0)
            view_mat = glm.lookAt((0.0, 0.0, 2.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
            model_mat = glm.lookAt((0.0, 0.0, 0.0), (context.x_rot, context.y_rot, -2.0), (0.0, 1.0, 0.0))

            hit = screen_to_board_pixels(context.input.mouse_pos, context.screen_size, model_mat, view_mat, proj_mat)
            if hit is not None and abs(hit[0]) <= 1.0 and abs(hit[1]) <= 1.0:
                self.board_widget.selected_cell = (int((hit[0] / 2 + 0.5) * self.board_widget.board.get_size()[0]),
                                                   int((-hit[1] / 2 + 0.5) * self.board_widget.board.get_size()[1]))

            # top_left_x = (context.screenSize[0] - self.board_pixel_size[0]) // 2
            # top_left_y = (context.screenSize[1] - self.board_pixel_size[1]) // 2
            #
            # mouse_x, mouse_y = context.input.mouse_pos
            #
            # if mouse_x <= top_left_x or mouse_x > top_left_x + self.board_pixel_size[0]:
            #     # mouse is outside board horizontally
            #     pass
            # elif mouse_y < top_left_y or mouse_y > top_left_y + self.board_pixel_size[1]:
            #     # mouse is outside board vertically
            #     pass
            # else:
            #     self.board_widget.selected_cell = ((mouse_x - top_left_x) // self.board_cell_pixel_size[0],
            #                                        (mouse_y - top_left_y) // self.board_cell_pixel_size[1])

        else:
            # mouse hasn't moved, defer to arrow keys
            while len(self.arrow_key_inputs) > 0:
                input_direction = self.arrow_key_inputs.pop(0)
                if self.board_widget.selected_cell[0] == -1 or self.board_widget.selected_cell[1] == -1:
                    self.board_widget.selected_cell = (4, 4)
                else:
                    match input_direction:
                        case ArrowKeyDirection.UP:
                            self.board_widget.selected_cell = (self.board_widget.selected_cell[0], max(self.board_widget.selected_cell[1] - 1, 0))
                        case ArrowKeyDirection.DOWN:
                            self.board_widget.selected_cell = (self.board_widget.selected_cell[0], min(self.board_widget.selected_cell[1] + 1, self.board_widget.board.get_size()[1] - 1))
                        case ArrowKeyDirection.RIGHT:
                            self.board_widget.selected_cell = (min(self.board_widget.selected_cell[0] + 1, self.board_widget.board.get_size()[0] - 1), self.board_widget.selected_cell[1])
                        case ArrowKeyDirection.LEFT:
                            self.board_widget.selected_cell = (max(self.board_widget.selected_cell[0] - 1, 0), self.board_widget.selected_cell[1])

        if previous != self.board_widget.selected_cell:
            hovered_x = self.board_widget.selected_cell[0] * self.board_cell_pixel_size[0] + self.board_cell_pixel_size[0] // 2
            hovered_y = self.board_widget.selected_cell[1] * self.board_cell_pixel_size[1] + self.board_cell_pixel_size[1] // 2

            if self.perspective_widget is None:
                top_left_x = (context.screen_size[0] - self.board_pixel_size[0]) // 2
                top_left_y = (context.screen_size[1] - self.board_pixel_size[1]) // 2

                hovered_x += top_left_x
                hovered_y += top_left_y

            # selection has changed, repaint
            self.positioned_widget.position = (hovered_x, hovered_y)
            self.positioned_widget.make_dirty()

            context.on_selection_changed(1.0 - self.board_widget.selected_cell[0] / 9, self.board_widget.selected_cell[1] / 9)


    def render(self, context: RenderContext):
        if self.board_widget.selected_cell[0] == -1 or self.board_widget.selected_cell[1] == -1:
            return

        if self.perspective_widget is not None:
            self.perspective_widget.x_rot = context.x_rot
            self.perspective_widget.y_rot = context.y_rot
            self.perspective_widget.draw_onto(context.surface, center=context.surface.get_rect().center)
        else:
            self.positioned_widget.draw_positioned(context.surface)


    def exit_scope(self, context: SceneChangeContext):
        context.input.remove_observer(self.__on_keyboard_input)

    def dispose(self):
        pass


def screen_to_board_pixels(
        mouse_pos: tuple[int, int],
        screen_size: tuple[int, int],
        model: glm.mat4,
        view: glm.mat4,
        proj: glm.mat4
) -> tuple[float, float] | None:
    """
    Convert a mouse position on the screen into a normalized coordinate (x, y) on a board defined by the given matrices.
    """

    viewport = glm.vec4(0, 0, screen_size[0], screen_size[1])
    mouse_y_inverted = screen_size[1] - mouse_pos[1]
    model_view = view * model

    near_point = glm.unProject(glm.vec3(mouse_pos[0], mouse_y_inverted, 0.0), model_view, proj, viewport)
    far_point = glm.unProject(glm.vec3(mouse_pos[0], mouse_y_inverted, 1.0), model_view, proj, viewport)

    ray_dir = glm.normalize(far_point - near_point)

    world_normal = glm.normalize((model * glm.vec4(0, 0, 1, 0)).xyz)
    plane_point_world = (model * glm.vec4(0, 0, 0, 1)).xyz

    denom = glm.dot(world_normal, ray_dir)
    if abs(denom) < 1e-8:
        # Ray is parallel to the plane
        return None

    t = glm.dot(world_normal, (plane_point_world - near_point)) / denom
    if t < 0:
        # Intersection is behind the camera
        return None

    intersection_world = near_point + t * ray_dir

    inv_model = glm.inverse(model)
    intersection_local = inv_model * glm.vec4(intersection_world.x, intersection_world.y, intersection_world.z, 1.0)

    board_x = intersection_local.x * (screen_size[0] / screen_size[1])
    board_y = intersection_local.y

    return board_x, board_y
