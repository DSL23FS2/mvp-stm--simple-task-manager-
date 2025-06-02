from .base_section import BaseSection
from nicegui import ui
from typing import Callable, Dict
from datetime import datetime
from ..fields.text.input import TextInput
from ..fields.datetime.input import DateTimeInput

class CreateSection(BaseSection):
    def __init__(self, on_create: Callable[[Dict], None]):
        self.on_create = on_create
        super().__init__('Создать задачу')

    def _create_content(self):
        with self.content:
            with ui.column().classes('w-full gap-4 px-2'):  # Added padding
                # Single line text input for task name
                self.name_input = TextInput(
                    label='Task Name',
                    placeholder='input task name here',
                )
                
                # Multiline text input for description
                self.description_input = TextInput(
                    label='Description',
                    placeholder='input task description here',
                    multiline=True
                )
                
                # DateTime input for deadline
                self.deadline_input = DateTimeInput(
                    label='Deadline'
                )
                
                with ui.row().classes('gap-2 justify-end w-full'):
                    ui.button(icon='check', on_click=self._handle_create).props('flat color=green')
                    ui.button(icon='close', on_click=self._clear_form).props('flat color=red')

    def _handle_create(self):
        name = self.name_input.get_value()
        if not name:
            ui.notify('Task name is required', type='negative')
            return

        task_data = {
            'name': name,
            'description': self.description_input.get_value(),
            'updated_at': self.deadline_input.get_value()
        }
        self.on_create(task_data)
        self._clear_form()

    def _clear_form(self):
        """Clear all input fields"""
        self.name_input.set_value('')
        self.description_input.set_value('')
        self.deadline_input.set_value(None)
