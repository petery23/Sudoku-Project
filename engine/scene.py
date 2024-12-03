from engine.contexts import UpdateContext, RenderContext, SceneChangeContext
from engine.system import System


class Scene:
    systems: list[System]

    def __init__(self, systems: list[System]):
        self.systems = systems

    def enter_scope(self, context: SceneChangeContext) -> None:
        for system in self.systems:
            system.enter_scope(context)

    def update(self, context: UpdateContext) -> None:
        for system in self.systems:
            system.update(context)

    def render(self, context: RenderContext) -> None:
        for system in self.systems:
            system.render(context)

    def exit_scope(self, context: SceneChangeContext) -> None:
        for system in self.systems:
            system.exit_scope(context)

    def dispose(self) -> None:
        for system in self.systems:
            system.dispose()