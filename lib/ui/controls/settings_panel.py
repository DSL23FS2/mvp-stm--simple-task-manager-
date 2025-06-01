from nicegui import ui

class SettingsPanel:
    def __init__(self):
        self.container = ui.column().classes('w-full p-4')
        self.container.visible = False
        self._create_ui()

    def _create_ui(self):
        with self.container:
            ui.label('Settings').classes('text-h3')

    def toggle(self):
        """Toggle panel visibility"""
        self.container.visible = not self.container.visible
