from datetime import datetime
from ...fields.base.field import UIField
from nicegui import ui

class DateTimeInput(UIField):
    def _create_ui(self):
        with self.container:
            ui.label(self.label).classes('text-sm text-gray-600')
            with ui.row().classes('w-full gap-2 items-end'):
                with ui.column().classes('flex-grow'):
                    self.date_input = ui.date().props('outlined').classes('w-full')
                with ui.column().classes('w-[140px]'):
                    self.time_input = ui.input(
                        label='Time',
                        value='12:00'
                    ).props('type=time outlined').classes('w-full')

    def get_value(self) -> datetime:
        if not self.date_input.value:
            return None
            
        hour, minute = map(int, self.time_input.value.split(':'))
        date_parts = self.date_input.value.split('-')
        
        return datetime(
            year=int(date_parts[0]),
            month=int(date_parts[1]),
            day=int(date_parts[2]),
            hour=hour,
            minute=minute
        )

    def set_value(self, value: datetime):
        if value:
            self.date_input.value = value.strftime('%Y-%m-%d')
            self.time_input.value = value.strftime('%H:%M')
        else:
            self.date_input.value = None
            self.time_input.value = '12:00'
