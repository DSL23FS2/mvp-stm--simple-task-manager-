from nicegui import ui

class BaseSection:
    def __init__(self, title: str):
        self.title = title
        self.container = ui.column().classes('w-full')
        self.content_visible = False
        self._create_ui()

    def _create_ui(self):
        with self.container:
            ui.button(self.title, on_click=self.toggle).classes('w-full')
            with ui.column().classes('w-full pl-4') as self.content:
                self._create_content()
        self.content.visible = False

    def toggle(self):
        self.content_visible = not self.content_visible
        self.content.visible = self.content_visible

    def _create_content(self):
        """Override this method to create section content"""
        pass
