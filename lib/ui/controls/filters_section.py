from nicegui import ui
from .base_section import BaseSection
from lib.ui.context.task_filter_context import TaskFilterContext
from data.models.task.validation import TaskQueryParams, SortOrder

class FiltersSection(BaseSection):
    def __init__(self, filter_context: TaskFilterContext):
        self.filter_context = filter_context
        super().__init__(title='Фильтры')
        # UI is created by BaseSection._create_ui

    def _create_content(self):
        """Override BaseSection's _create_content"""
        with self.content:
            with ui.column().classes('gap-4 w-full'):
                self.name_filter = ui.input(label='Task Name Filter')
                self.status_filter = ui.select(
                    options={
                        None: 'All',
                        True: 'Completed',
                        False: 'In Progress'
                    },
                    value=None,
                    label='Status Filter'
                )
                self.sort_by = ui.select(
                    options={
                        'created_at': 'Creation Date',
                        'name': 'Name'
                    },
                    value='created_at',
                    label='Sort By'
                )
                self.order = ui.select(
                    options={
                        SortOrder.asc: 'Ascending',
                        SortOrder.desc: 'Descending'
                    },
                    value=SortOrder.asc,
                    label='Order'
                )
                ui.button('Apply Filters', on_click=self._apply_filters)

    def _apply_filters(self):
        params = TaskQueryParams(
            name=self.name_filter.value if self.name_filter.value else None,
            is_completed=self.status_filter.value,
            sort_by=self.sort_by.value,
            order=self.order.value
        )
        self.filter_context.update_filter(params)
