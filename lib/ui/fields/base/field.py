from nicegui import ui
from typing import Any, Optional, Callable

class UIField:
    def __init__(self, 
                 label: str,
                 value: Any = None,
                 placeholder: str = '',
                 on_change: Optional[Callable[[Any], None]] = None):
        self.label = label
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        self.container = ui.column().classes('w-full')
        self._create_ui()

    def _create_ui(self):
        with self.container:
            ui.label(self.label).classes('text-sm text-gray-600')

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any):
        self.value = value
        self._update_ui()

    def _update_ui(self):
        """Override this method to update UI when value changes"""
        pass
