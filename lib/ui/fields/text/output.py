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
                self.output = ui.textarea(
                    value='',
                ).props('readonly dense').classes('w-full bg-gray-50')
            else:
                # Используем paragraph вместо label для лучшего отображения
                self.output = ui.label('').classes('block mt-1 text-gray-900')
            self._update_ui()

    def _update_ui(self):
        """Update displayed text"""
        display_value = str(self.value) if self.value is not None else '-'
        display_value = display_value.strip()
        if not display_value:
            display_value = '-'
            
        if hasattr(self, 'output'):
            if self.multiline:
                self.output.value = display_value
            else:
                self.output.text = display_value

    def set_value(self, value: str):
        self.value = value
        self._update_ui()
