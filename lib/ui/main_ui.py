from nicegui import ui
from lib.ui.context.task_filter_context import TaskFilterContext
from lib.ui.controls import TaskListUI, FiltersSection, CreateSection

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
        self.filter_context = TaskFilterContext()
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
                        # Создаем секции - они сразу отобразятся благодаря BaseSection
                        self.filters_section = FiltersSection(self.filter_context)
                        self.task_list = TaskListUI(self.filter_context)
                        # Initial load using default filter
                        self.task_list.refresh_tasks()
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
