from .base_section import BaseSection
from nicegui import ui
from typing import Callable, Dict
from datetime import datetime

class CreateSection(BaseSection):
    def __init__(self, on_create: Callable[[Dict], None]):
        self.on_create = on_create
        super().__init__('Создать задачу')

    def _create_content(self):
        with self.content:
            with ui.column().classes('w-full gap-4 px-2'):  # Added padding
                self.name_input = ui.input(
                    label='Task Name',
                    placeholder='Введите название задачи'
                ).classes('w-full')
                
                self.description_input = ui.textarea(
                    label='Description'
                ).classes('w-full')
                
                with ui.column().classes('w-full gap-2'):
                    ui.label('Deadline Date & Time').classes('text-sm text-gray-600')
                    with ui.row().classes('w-full gap-2 items-end'):
                        with ui.column().classes('flex-grow'):
                            self.date_input = ui.date().props('outlined').classes('w-full')
                        with ui.column().classes('w-[140px]'):
                            # Fixed time input to use props instead of type
                            self.time_input = ui.input(
                                label='Time',
                                value='00:00'
                            ).props('type=time outlined').classes('w-full')
                
                with ui.row().classes('gap-2 justify-end w-full'):
                    ui.button(icon='check', on_click=self._handle_create).props('flat color=green')
                    ui.button(icon='close', on_click=self._clear_form).props('flat color=red')

    def _handle_create(self):
        name = self.name_input.value.strip() if self.name_input.value else None
        if not name:
            ui.notify('Task name is required', type='negative')
            return

        deadline = None
        if self.date_input.value and self.time_input.value:
            # Parse time string (HH:MM)
            hour, minute = map(int, self.time_input.value.split(':'))
            # Parse date string (YYYY-MM-DD)
            date_parts = self.date_input.value.split('-')
            # Create Python datetime object
            deadline = datetime(
                year=int(date_parts[0]),
                month=int(date_parts[1]),
                day=int(date_parts[2]),
                hour=hour,
                minute=minute
            )

        task_data = {
            'name': name,
            'description': self.description_input.value.strip() or None,
            'updated_at': deadline  # Now sending Python datetime object directly
        }
        self.on_create(task_data)
        self._clear_form()

    def _clear_form(self):
        self.name_input.value = ''
        self.description_input.value = ''
        self.date_input.value = None
        self.time_input.value = '00:00'
