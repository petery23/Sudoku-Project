from engine.contexts import UpdateContext, RenderContext
from engine.system import System
from engine.widget import PositionedWidget


class DrawSystem(System):
    widgets: list[PositionedWidget]

    def __init__(self, widgets: list[PositionedWidget]):
        self.widgets = widgets

    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        pass

    def render(self, context: RenderContext):
        for widget in self.widgets:
            widget.draw_positioned(context.surface)

    def exit_scope(self):
        pass

    def dispose(self):
        pass