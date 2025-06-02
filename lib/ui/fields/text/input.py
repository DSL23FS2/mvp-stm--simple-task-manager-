from ...fields.base.field import UIField
from nicegui import ui

class TextInput(UIField):
    def __init__(self, 
                 label: str,
                 value: str = '',
                 placeholder: str = '',
                 multiline: bool = False,
                 **kwargs):
        self.multiline = multiline
        super().__init__(label, value, placeholder, **kwargs)

    def _create_ui(self):
        super()._create_ui()
        with self.container:
            if self.multiline:
                self.input = ui.textarea(
                    value=self.value,
                    placeholder=self.placeholder
                ).props('outlined').classes('w-full')
            else:
                self.input = ui.input(
                    value=self.value,
                    placeholder=self.placeholder
                ).props('outlined').classes('w-full')

    def get_value(self) -> str:
        return self.input.value.strip() if self.input.value else None

    def set_value(self, value: str):
        self.input.value = value or ''
