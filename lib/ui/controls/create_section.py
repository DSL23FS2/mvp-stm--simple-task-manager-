from .base_section import BaseSection
from nicegui import ui
from typing import Callable, Dict

class CreateSection(BaseSection):
    def __init__(self, on_create: Callable[[Dict], None]):
        self.on_create = on_create
        super().__init__('Create Task')

    def _create_content(self):
        self.name_input = ui.input(label='Task Name')
        self.description_input = ui.textarea(label='Description').classes('w-full')
        
        # Create labeled date input
        with ui.column().classes('w-full'):
            ui.label('Deadline')
            self.deadline_input = ui.date()
        
        with ui.row().classes('gap-2 justify-end'):
            ui.button(icon='check', on_click=self._handle_create).props('flat color=green')
            ui.button(icon='close', on_click=self._clear_form).props('flat color=red')

    def _handle_create(self):
        name = self.name_input.value.strip() if self.name_input.value else None
        if not name:
            ui.notify('Task name is required', type='negative')
            return

        task_data = {
            'name': name,
            'description': self.description_input.value.strip() or None,
            'updated_at': self.deadline_input.value
        }
        self.on_create(task_data)
        self._clear_form()

    def _clear_form(self):
        self.name_input.value = ''
        self.description_input.value = ''
        self.deadline_input.value = None
