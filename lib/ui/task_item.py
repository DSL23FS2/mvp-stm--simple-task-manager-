from nicegui import ui
from datetime import datetime
from typing import Callable

class TaskItemUI:
    def __init__(self, task_data: dict, on_delete: Callable[[int], None], on_refresh: Callable[[], None]):
        self.task = task_data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        self.expanded = False
        self.container = ui.column().classes('w-full')
        self._create_ui()

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m-%d %H:%M") if date else "-"

    def toggle_details(self):
        self.expanded = not self.expanded
        self.details_container.set_visibility(self.expanded)

    def _create_ui(self):
        # Основная строка
        with self.container:
            with ui.row().classes('w-full items-center justify-between p-2 border rounded'):
                # Левая часть с информацией
                with ui.row().classes('gap-8 items-center'):
                    ui.label(self.task['name']).classes('text-lg min-w-40')
                    ui.label(self.format_date(self.task['updated_at'])).classes('min-w-40')
                    ui.label('✓' if self.task['is_completed'] else '○').classes('min-w-8')
                
                # Правая часть с кнопками
                with ui.row().classes('gap-2'):
                    ui.button(icon='expand_more', on_click=self.toggle_details).props('flat')
                    ui.button(icon='delete', on_click=lambda: self._handle_delete()).props('flat color=red')

            # Контейнер с деталями
            self.details_container = ui.column().classes('w-full p-4 bg-gray-50 border-x border-b rounded-b')
            with self.details_container:
                ui.label(f"Task Name: {self.task['name']}")
                ui.label(f"Start Date: {self.format_date(self.task['created_at'])}")
                ui.label(f"End Date: {self.format_date(self.task['updated_at'])}")
                if self.task['description']:
                    ui.label(f"Description: {self.task['description']}")
                ui.label(f"Status: {'Completed' if self.task['is_completed'] else 'In Progress'}")

            self.details_container.set_visibility(False)

    def _handle_delete(self):
        self.on_delete(self.task['id'])
        self.on_refresh()
