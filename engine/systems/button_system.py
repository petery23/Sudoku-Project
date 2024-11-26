from engine.engine import UpdateContext, RenderContext
from engine.system import System
from engine.widgets.button import Button


class ButtonSystem(System):
    buttons: list[Button]

    def __init__(self, buttons: list[Button]):
        self.buttons = buttons

    def enter_scope(self):
        pass

    def update(self, context: UpdateContext):
        for click in context.input.clicks:
            for button in self.buttons:
                if not button.interactable: continue
                if not button.rect.collidepoint(click): continue
                button.on_click()


    def render(self, context: RenderContext):
        for button in self.buttons:
            button.draw_positioned(context.surface)


    def exit_scope(self):
        pass

    def dispose(self):
        pass