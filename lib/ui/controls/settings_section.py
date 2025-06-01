from .base_section import BaseSection
from nicegui import ui

class SettingsSection(BaseSection):
    def __init__(self):
        super().__init__('Settings')

    def _create_content(self):
        ui.label('Settings Content').classes('text-h6')
