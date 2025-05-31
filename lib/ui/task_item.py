from nicegui import ui
from datetime import datetime
from typing import Callable

class TaskItemUI:
    # Константы для размеров (можно вынести в конфигурацию)
    CONTAINER_WIDTH = 'w-[800px]'  # Фиксированная ширина контейнера
    ROW_HEIGHT = 'h-[64px]'        # Фиксированная высота строки
    DETAILS_HEIGHT = 'h-[240px]'   # Фиксированная высота области деталей

    def __init__(self, task_data: dict, on_delete: Callable[[int], None], on_refresh: Callable[[], None]):
        # Инициализация основных параметров
        self.task = task_data
        self.on_delete = on_delete
        self.on_refresh = on_refresh
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
        self.details_container.set_visibility(self.expanded)

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

            # Контейнер с деталями (фиксированная высота)
            self.details_container = ui.column().classes(
                f'w-full p-4 bg-gray-50 border-x border-b rounded-b {self.DETAILS_HEIGHT}'
                ' overflow-y-auto'
            )
            with self.details_container:
                # Детальная информация с корректным переносом текста
                self._create_detail_row("Task Name", self.task['name'])
                self._create_detail_row("Start Date", self.format_date(self.task['created_at']))
                self._create_detail_row("End Date", self.format_date(self.task['updated_at']))
                if self.task['description']:
                    self._create_detail_row("Description", self.task['description'])
                self._create_detail_row("Status", 'Completed' if self.task['is_completed'] else 'In Progress')

            # Скрываем детали по умолчанию
            self.details_container.set_visibility(False)

    def _create_detail_row(self, label: str, value: str):
        """Создание строки с детальной информацией"""
        with ui.row().classes('w-full gap-4 py-2'):
            ui.label(f"{label}:").classes('font-bold w-[128px]')
            # Контейнер для значения с фиксированной шириной и переносом текста
            with ui.element('div').classes('w-[600px]'):
                ui.label(str(value)).classes('break-words')

    def _handle_delete(self):
        """Обработка удаления задачи"""
        self.on_delete(self.task['id'])
        self.on_refresh()
