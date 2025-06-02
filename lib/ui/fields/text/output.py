from ...fields.base.field import UIField
from nicegui import ui

class TextOutput(UIField):
    def __init__(self, label: str, value: str = '', multiline: bool = False, **kwargs):
        self.multiline = multiline
        super().__init__(label, value, **kwargs)

    def _create_ui(self):
        with self.container:
            ui.label(self.label).classes('text-sm text-gray-600')
            if self.multiline:
                # Use props for readonly state and styling
                self.output = ui.textarea(
                    value='',  # Will be set in _update_ui
                ).props('readonly dense').classes('w-full bg-gray-50')
            else:
                self.output = ui.label().classes('mt-1')
            self._update_ui()

    def _update_ui(self):
        """Update displayed text"""
        display_value = str(self.value) if self.value is not None else '-'
        display_value = display_value.strip()
        if not display_value:
            display_value = '-'
            
        if hasattr(self, 'output'):
            self.output.value = display_value

    def set_value(self, value: str):
        self.value = value
        self._update_ui()
