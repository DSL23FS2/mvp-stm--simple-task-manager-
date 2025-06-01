from nicegui import ui
from .task_list import TaskListUI
from .controls.settings_section import SettingsSection
from .controls.filters_section import FiltersSection
from .controls.create_section import CreateSection

class MainUI:
    # Базовые размеры
    BASE_WIDTH = 800
    SCROLLBAR_WIDTH = 24
    
    # Константы для размеров и стилей
    CONTAINER_WIDTH = f'w-[{BASE_WIDTH}px]'
    SCROLL_CONTAINER_WIDTH = f'w-[{BASE_WIDTH + SCROLLBAR_WIDTH}px]'
    HEADER_HEIGHT = 'h-[48px]'
    # Высота контента: 100vh минус высота header (48px), заголовок (48px) и отступы (16px)
    CONTENT_HEIGHT = 'h-[calc(100vh-112px)]'

    def __init__(self):
        self.container = ui.column().classes(f'{self.SCROLL_CONTAINER_WIDTH} ml-4')
        self._create_ui()

    def _create_header(self):
        """Создание фиксированного заголовка"""
        # Используем CONTENT_WIDTH для внутреннего контента
        with ui.row().classes(f'{self.CONTAINER_WIDTH} {self.HEADER_HEIGHT} items-center border-b bg-gray-100'):
            # Названия столбцов с фиксированными размерами
            ui.label('Task Name').classes('w-[300px] font-bold')
            ui.label('End Date').classes('w-[160px] font-bold')
            ui.label('Status').classes('w-[32px] font-bold')
            # Пустое пространство для кнопок
            ui.element('div').classes('w-[96px]')

    def _create_ui(self):
        """Создание основного интерфейса"""
        with ui.row().classes('w-full gap-4'):
            # Левая панель с задачами
            with ui.column().classes(f'{self.SCROLL_CONTAINER_WIDTH} ml-4'):
                # Заголовок приложения
                ui.label('Task Manager').classes('text-h4 q-mb-md')
                
                # Фиксированный заголовок таблицы
                self._create_header()
                
                # Область прокрутки с фиксированной шириной
                with ui.scroll_area().classes(f'{self.SCROLL_CONTAINER_WIDTH} {self.CONTENT_HEIGHT}'):
                    with ui.column().classes(f'{self.CONTAINER_WIDTH}'):
                        self.task_list = TaskListUI()
                        self.task_list.create()

            # Правая панель управления
            with ui.column().classes('flex-grow h-full max-w-md gap-4'):
                # Кнопки управления
                with ui.row().classes('w-full gap-2 justify-center q-mb-md'):
                    for btn_data in [
                        ('Settings', self._toggle_settings),
                        ('Filters', self._toggle_filters),
                        ('Create', self._toggle_create)
                    ]:
                        ui.button(btn_data[0], on_click=btn_data[1]).classes('w-32')

                # Панели управления
                with ui.scroll_area().classes(f'w-full {self.CONTENT_HEIGHT}'):
                    self.settings_section = SettingsSection()
                    self.filters_section = FiltersSection(self.task_list.refresh_tasks)
                    self.create_section = CreateSection(self.task_list.create_task)

    def _toggle_settings(self):
        self.settings_section.toggle()
        self.filters_section.container.style('display: none')
        self.create_section.container.style('display: none')

    def _toggle_filters(self):
        self.settings_section.container.style('display: none')
        self.filters_section.toggle()
        self.create_section.container.style('display: none')

    def _toggle_create(self):
        self.settings_section.container.style('display: none')
        self.filters_section.container.style('display: none')
        self.create_section.toggle()

    def create(self):
        return self.container
