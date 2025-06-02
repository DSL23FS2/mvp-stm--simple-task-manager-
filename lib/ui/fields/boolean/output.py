from ...fields.base.field import UIField
from nicegui import ui

class BooleanOutput(UIField):
    def __init__(self, label: str, value: bool = False, use_icon: bool = False, **kwargs):
        self.use_icon = use_icon
        super().__init__(label, value, **kwargs)

    def _create_ui(self):
        with self.container:
            ui.label(self.label).classes('text-sm text-gray-600')
            if self.use_icon:
                # Initialize icon with initial value
                initial_icon = 'check_circle' if self.value else 'cancel'
                self.output = ui.icon(name=initial_icon).classes(
                    'text-green-600' if self.value else 'text-red-600'
                )
            else:
                self.output = ui.label(
                    text='Completed' if self.value else 'In Progress'
                ).classes('text-green-600' if self.value else 'text-orange-600')

    def _update_ui(self):
        """Update displayed status"""
        if self.use_icon:
            self.output.name = 'check_circle' if self.value else 'cancel'
            self.output.classes('text-green-600' if self.value else 'text-red-600', replace=True)
        else:
            self.output.text = 'Completed' if self.value else 'In Progress'
            self.output.classes('text-green-600' if self.value else 'text-orange-600', replace=True)

    def set_value(self, value: bool):
        """Override set_value to handle boolean specifically"""
        self.value = bool(value)
        self._update_ui()
