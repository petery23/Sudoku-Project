import math

import pygame, random

from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.scene import Scene
from engine.system import System
from game.widgets.sudoku_board_widget import SudokuBoardWidget

BLACK = (0, 0, 0)
PERSPECTIVE_IDLE_INTENSITY = 0.175
PERSPECTIVE_MOUSE_INTENSITY = 0.225
PERSPECTIVE_FOV = 60.0

IDLE_DELAY = 2
IDLE_TRANSITION_TIME = 0.35

class GameScene(Scene):
    background: pygame.Surface

    board_cell_pixel_size: tuple[int, int]
    board_pixel_size: tuple[int, int]

    idle_delay = 0.0

    x_rot_velocity = 0.0
    y_rot_velocity = 0.0

    x_rot_target = 0.0
    y_rot_target = 0.0

    x_rot = 0.0
    y_rot = 0.0

    fun_multiplier = 1.0

    def __init__(self, window_size: tuple[int, int], board_widget: SudokuBoardWidget, systems: list[System]) -> None:
        super().__init__(systems)
        self.lines = []
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, window_size)

        self.board_pixel_size = board_widget.get_size()
        self.board_cell_pixel_size = (self.board_pixel_size[0] // board_widget.board.get_size()[0], self.board_pixel_size[1] // board_widget.get_size()[1])


    def enter_scope(self, context: SceneChangeContext) -> None:
        self.lines = [[random.uniform(0.0, 1.0), random.uniform(-1.0, 1.0)] for _ in range(50)]
        super().enter_scope(context)


    def update(self, context: UpdateContext) -> None:
        for line in self.lines:
            line[1] += 0.5 * context.dt
            if line[1] > 1.0:
                line[1] = random.uniform(-0.5, 0)

        if abs(context.input.mouse_delta[0]) + abs(context.input.mouse_delta[1]) >= 1:
            # mouse moved

            top_left_x = (context.screen_size[0] - self.board_pixel_size[0]) // 2
            top_left_y = (context.screen_size[1] - self.board_pixel_size[1]) // 2

            mouse_x, mouse_y = context.input.mouse_pos

            if mouse_x <= top_left_x or mouse_x > top_left_x + self.board_pixel_size[0]:
                # mouse is outside board horizontally
                pass
            elif mouse_y < top_left_y or mouse_y > top_left_y + self.board_pixel_size[1]:
                # mouse is outside board vertically
                pass
            else:
                self.idle_delay = IDLE_DELAY

                self.x_rot_target = lerp(-PERSPECTIVE_MOUSE_INTENSITY, PERSPECTIVE_MOUSE_INTENSITY, 1.0 - (mouse_x - top_left_x) / self.board_pixel_size[0])
                self.y_rot_target = lerp(-PERSPECTIVE_MOUSE_INTENSITY, PERSPECTIVE_MOUSE_INTENSITY, (mouse_y - top_left_y) / self.board_pixel_size[1])

        if self.idle_delay > 0:
            self.idle_delay -= context.dt
        else:
            # user is idle
            self.x_rot_target = math.cos(context.time) * PERSPECTIVE_IDLE_INTENSITY
            self.y_rot_target = math.sin(context.time) * PERSPECTIVE_IDLE_INTENSITY

        self.x_rot, self.x_rot_velocity = smooth_damp(self.x_rot, self.x_rot_target, self.x_rot_velocity, IDLE_TRANSITION_TIME, 100000.0, context.dt)
        self.y_rot, self.y_rot_velocity = smooth_damp(self.y_rot, self.y_rot_target, self.y_rot_velocity, IDLE_TRANSITION_TIME, 100000.0, context.dt)

        context.x_rot = self.x_rot * self.fun_multiplier
        context.y_rot = self.y_rot * self.fun_multiplier

        def on_selection_changed(norm_x: float, norm_y: float) -> None:
            self.idle_delay = IDLE_DELAY

            self.x_rot_target = lerp(-PERSPECTIVE_MOUSE_INTENSITY, PERSPECTIVE_MOUSE_INTENSITY, norm_x)
            self.y_rot_target = lerp(-PERSPECTIVE_MOUSE_INTENSITY, PERSPECTIVE_MOUSE_INTENSITY, norm_y)

        context.on_selection_changed = on_selection_changed

        super().update(context)


    def render(self, context: RenderContext) -> None:
        context.surface.fill(BLACK)

        width = context.surface.get_width()
        height = context.surface.get_height()

        context.x_rot = self.x_rot * self.fun_multiplier
        context.y_rot = self.y_rot * self.fun_multiplier

        for line in self.lines:
            start = (line[0] * width, line[1] * height)
            end = (line[0] * width, line[1] * height + 50)
            pygame.draw.line(context.surface, (128,0,128), start, end, 2)

        super().render(context)


    def exit_scope(self, context: SceneChangeContext) -> None:
        super().exit_scope(context)

    def dispose(self) -> None:
        super().dispose()


def lerp(x1: float, x2: float, t: float):
    return x1 + (x2 - x1) * t


def clamp(x: float, minimum: float, maximum: float) -> float:
    return max(min(x, maximum), minimum)


def smooth_damp(current: float,
                target: float,
                current_velocity: float,
                smooth_time: float,
                max_speed: float,
                delta_time: float) -> (float, float):
    """

    Smoothing function based on Unity's Mathf.SmoothDamp

    Args:
        current:
        target:
        current_velocity:
        smooth_time:
        max_speed:
        delta_time:

    Returns:
        next:
        new_velocity:

    """

    smooth_time = max(0.0001, smooth_time)
    num = 2 / smooth_time
    num2 = num * delta_time
    num3 = 1 / (1 + num2 + 0.48 * num2 * num2 + 0.235 * num2 * num2 * num2)
    num4 = current - target
    num5 = target
    num6 = max_speed * smooth_time
    num4 = clamp(num4, -num6, num6)
    target = current - num4
    num7 = (current_velocity + num * num4) * delta_time
    new_velocity = (current_velocity - num * num7) * num3
    num8 = target + (num4 + num7) * num3
    if num5 - current > 0 == num8 > num5:
        num8 = num5
        new_velocity = (num8 - num5) / delta_time

    return num8, new_velocity