from datetime import datetime
from ...fields.base.field import UIField
from nicegui import ui

class DateTimeOutput(UIField):
    def __init__(self, label: str, value: datetime = None, format: str = '%Y-%m-%d %H:%M', **kwargs):
        self.format = format
        super().__init__(label, value, **kwargs)

    def _create_ui(self):
        with self.container:
            ui.label(self.label).classes('text-sm text-gray-600')
            self.output = ui.label().classes('text-gray-900')
            self._update_ui()

    def _update_ui(self):
        """Update displayed datetime"""
        if isinstance(self.value, datetime):
            self.output.text = self.value.strftime(self.format)
        else:
            self.output.text = '-'

    def set_value(self, value: datetime):
        """Override set_value to handle datetime specifically"""
        self.value = value
        self._update_ui()
