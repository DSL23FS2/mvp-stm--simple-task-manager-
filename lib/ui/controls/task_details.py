from nicegui import ui
from datetime import datetime
from typing import Callable, Dict, Any

class TaskDetailsUI:
    def __init__(self, task_data: dict, on_update: Callable[[int, Dict[str, Any]], None]):
        self.task = task_data
        self.on_update = on_update
        self.edit_mode = False
        self.edited_data = {}
        self.container = ui.column().classes(
            'w-full p-4 bg-gray-50 border-x border-b rounded-b'
        )
        self._create_ui()

    def _create_field(self, label: str, value: str) -> Dict[str, ui.element]:
        field_container = ui.row().classes('w-full gap-4 py-2')
        with field_container:
            label_elem = ui.label(f"{label}:").classes('font-bold w-[128px]')
            value_container = ui.element('div').classes('w-[600px]')
            with value_container:
                display_elem = ui.label(str(value)).classes('break-words')
                edit_elem = ui.input(value=str(value)).classes('w-full')
                # Начально скрываем поле редактирования
                edit_elem.visible = False

        return {
            'container': field_container,
            'label': label_elem,
            'display': display_elem,
            'edit': edit_elem
        }

    def _create_ui(self):
        with self.container:
            # Поля для отображения/редактирования
            self.name_field = self._create_field("Task Name", self.task.get('name', '-'))
            self.created_field = self._create_field("Start Date", self.format_date(self.task.get('created_at', '-')))
            self.updated_field = self._create_field("End Date", self.format_date(self.task.get('updated_at', '-')))
            self.description_field = self._create_field("Description", self.task.get('description', '-'))
            self.status_field = self._create_field("Status", 'Completed' if self.task.get('is_completed') else 'In Progress')

            # Кнопки управления
            with ui.row().classes('w-full justify-end gap-2 mt-2'):
                self.edit_btn = ui.button('Edit', on_click=self._start_edit).props('outline')
                with ui.row().classes('gap-2') as self.action_buttons:
                    self.save_btn = ui.button(icon='check', on_click=self._save_changes).props('flat color=green')
                    self.cancel_btn = ui.button(icon='close', on_click=self._cancel_edit).props('flat color=red')
                self.action_buttons.visible = False

    def _start_edit(self):
        self.edit_mode = True
        self.edit_btn.visible = False
        self.action_buttons.visible = True
        for field in [self.name_field, self.description_field]:
            field['display'].visible = False
            field['edit'].visible = True

    def _end_edit(self):
        self.edit_mode = False
        self.edit_btn.visible = True
        self.action_buttons.visible = False
        for field in [self.name_field, self.description_field]:
            field['display'].visible = True
            field['edit'].visible = False

    def _save_changes(self):
        self.edited_data = {
            'name': self.name_field['edit'].value,
            'description': self.description_field['edit'].value,
        }
        self.on_update(self.task['id'], self.edited_data)
        self._end_edit()

    def _cancel_edit(self):
        # Восстанавливаем исходные значения
        self.name_field['edit'].value = self.task.get('name', '-')
        self.description_field['edit'].value = self.task.get('description', '-')
        self._end_edit()

    def format_date(self, date: datetime) -> str:
        """Форматирование даты с проверкой на None"""
        return date.strftime("%Y-%m-%d %H:%M") if date else "-"
