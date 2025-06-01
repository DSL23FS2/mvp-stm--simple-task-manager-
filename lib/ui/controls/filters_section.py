from .base_section import BaseSection
from nicegui import ui
from typing import Callable
from data.models.task.validation import TaskQueryParams

class FiltersSection(BaseSection):
    def __init__(self, on_filter: Callable[[TaskQueryParams], None]):
        self.on_filter = on_filter
        super().__init__('Filters')

    def _create_content(self):
        self.name_filter = ui.input(label='Task Name Filter')
        self.status_filter = ui.select(
            options=[
                {'label': 'All', 'value': None},
                {'label': 'Completed', 'value': True},
                {'label': 'In Progress', 'value': False}
            ],
            label='Status Filter'
        )
        self.sort_by = ui.select(
            options=[
                {'label': 'Creation Date', 'value': 'created_at'},
                {'label': 'Name', 'value': 'name'}
            ],
            label='Sort By'
        )
        self.order = ui.select(
            options=[
                {'label': 'Ascending', 'value': 'asc'},
                {'label': 'Descending', 'value': 'desc'}
            ],
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
        self.on_filter(params)
