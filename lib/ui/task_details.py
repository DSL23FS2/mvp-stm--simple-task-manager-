from nicegui import ui
from datetime import datetime
from typing import Callable, Dict, Any

class TaskDetailsUI:
    def __init__(self, task_data: dict, on_update: Callable[[int, Dict[str, Any]], None]):
        self.task = task_data
        self.on_update = on_update
        self.edit_mode = False
        self.edited_data = {}
        self.fields = {}  # Store field references
        self.container = ui.column().classes(
            'w-full p-4 bg-gray-50 border-x border-b rounded-b'
            ' overflow-y-auto'
        )
        self._create_ui()

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m-%d %H:%M") if date else "-"

    def _create_ui(self):
        with self.container:
            # Поля для отображения/редактирования
            self.name_field = self._create_field("Task Name", self.task.get('name', '-'))
            self.created_field = self._create_field("Start Date", self.format_date(self.task.get('created_at')))
            self.updated_field = self._create_field("End Date", self.format_date(self.task.get('updated_at')))
            self.description_field = self._create_field("Description", self.task.get('description', '-'))
            self.status_field = self._create_field("Status", 'Completed' if self.task.get('is_completed') else 'In Progress')

            # Кнопки управления редактированием
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                self.edit_btn = ui.button('Edit', on_click=self._start_edit).props('outline')
                with ui.row().classes('gap-2').bind_visibility_from(self, 'edit_mode'):
                    ui.button(icon='check', on_click=self._save_changes).props('flat color=green')
                    ui.button(icon='close', on_click=self._cancel_edit).props('flat color=red')

    def _create_field(self, label: str, value: str) -> Dict[str, ui.element]:
        field_container = ui.row().classes('w-full gap-4 py-2')
        with field_container:
            label_elem = ui.label(f"{label}:").classes('font-bold w-[128px]')
            value_container = ui.element('div').classes('w-[600px]')
            with value_container:
                display_elem = ui.label(str(value)).classes('break-words')
                edit_elem = ui.input(value=str(value)).classes('w-full')
                edit_elem.visible = False  # Set initial visibility

        return {
            'container': field_container,
            'label': label_elem,
            'display': display_elem,
            'edit': edit_elem
        }

    def _start_edit(self):
        self.edit_mode = True
        for field in [self.name_field, self.description_field]:
            field['display'].visible = False
            field['edit'].visible = True

    def _save_changes(self):
        self.edited_data = {
            'name': self.name_field['edit'].value,
            'description': self.description_field['edit'].value,
        }
        self.on_update(self.task['id'], self.edited_data)
        self._end_edit()

    def _cancel_edit(self):
        self._end_edit()

    def _end_edit(self):
        self.edit_mode = False
        for field in [self.name_field, self.description_field]:
            field['display'].visible = True
            field['edit'].visible = False
