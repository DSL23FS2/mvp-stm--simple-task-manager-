from nicegui import ui
from datetime import datetime
from typing import Callable
from .task_details import TaskDetailsUI

class TaskItemUI:
    # Константы для размеров (можно вынести в конфигурацию)
    CONTAINER_WIDTH = 'w-[800px]'  # Фиксированная ширина контейнера
    ROW_HEIGHT = 'h-[64px]'        # Фиксированная высота строки
    DETAILS_HEIGHT = 'h-[240px]'   # Фиксированная высота области деталей

    def __init__(
        self, 
        task_data: dict, 
        on_delete: Callable[[int], None], 
        on_refresh: Callable[[], None],
        on_update: Callable[[int, dict], None]
    ):
        # Инициализация основных параметров
        self.task = task_data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
        self.on_update = on_update
        self.expanded = False
        # Основной контейнер с фиксированной шириной
        self.container = ui.column().classes(f'{self.CONTAINER_WIDTH} mx-auto')
        self._create_ui()

    def format_date(self, date: datetime) -> str:
        """Форматирование даты с проверкой на None"""
        return date.strftime("%Y-%m-%d %H:%M") if date else "-"

    def toggle_details(self):
        """Переключение видимости детальной информации"""
        self.expanded = not self.expanded
        if hasattr(self, 'details_container'):
            self.details_container.visible = self.expanded

    def _create_ui(self):
        """Создание UI элементов"""
        with self.container:
            # Основная строка с фиксированной высотой
            with ui.row().classes(f'w-full items-center justify-between p-2 border rounded {self.ROW_HEIGHT}'):
                # Левая часть с информацией
                with ui.row().classes('gap-8 items-center flex-grow'):
                    # Название задачи
                    with ui.element('div').classes('w-[300px]'):
                        ui.label(self.task['name']).classes('text-lg truncate')
                    # Дата с фиксированной шириной
                    ui.label(self.format_date(self.task['updated_at'])).classes('w-[160px]')
                    # Статус
                    ui.label('✓' if self.task['is_completed'] else '○').classes('w-[32px] text-center')
                
                # Кнопки управления
                with ui.row().classes('gap-2 w-[96px] justify-end'):
                    ui.button(icon='expand_more', on_click=self.toggle_details).props('flat dense')
                    ui.button(icon='delete', on_click=lambda: self._handle_delete()).props('flat dense color=red')

            # Create details UI
            details_ui = TaskDetailsUI(
                task_data=self.task,
                on_update=self._handle_update
            )
            self.details_container = details_ui.container
            self.details_container.visible = False  # Use visible property directly

    def _handle_update(self, task_id: int, updated_data: dict):
        """Обработка обновления задачи"""
        self.on_update(task_id, updated_data)
        self.on_refresh()  # Просто вызываем refresh без параметров

    def _handle_delete(self):
        """Обработка удаления задачи"""
        self.on_delete(self.task['id'])
        self.on_refresh()
