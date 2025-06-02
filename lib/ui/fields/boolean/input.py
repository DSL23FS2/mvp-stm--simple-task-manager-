from ...fields.base.field import UIField
from nicegui import ui

class BooleanInput(UIField):
    def _create_ui(self):
        super()._create_ui()
        with self.container:
            self.input = ui.switch(
                text='',
                value=bool(self.value)
            ).classes('mt-1')
            if self.on_change:
                self.input.on('change', lambda e: self.on_change(e.value))

    def get_value(self) -> bool:
        return bool(self.input.value)

    def set_value(self, value: bool):
        self.input.value = bool(value)
