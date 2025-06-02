from nicegui import ui
from datetime import datetime
from typing import Dict, Any, Callable
from ..fields.text.input import TextInput
from ..fields.text.output import TextOutput
from ..fields.datetime.input import DateTimeInput
from ..fields.datetime.output import DateTimeOutput
from ..fields.boolean.output import BooleanOutput

class TaskDetailsUI:
    def __init__(self, task_data: dict, on_update: Callable[[int, Dict[str, Any]], None]):
        self.task = task_data
        self.on_update = on_update
        self.edit_mode = False
        
        # Create main container
        self.container = ui.card().classes('w-full')
        
        # Create view and edit panels
        with self.container:
            self.view_panel = ui.column().classes('w-full p-4 gap-4')
            self.edit_panel = ui.column().classes('w-full p-4 gap-4')
            
            # Create content for both panels
            self._create_view_panel()
            self._create_edit_panel()
            
            # Action buttons row
            with ui.row().classes('w-full justify-end gap-2 px-4 pb-2'):
                self.edit_btn = ui.button('Edit', on_click=self._start_edit).props('outline')
                with ui.row().classes('gap-2') as self.action_buttons:
                    ui.button(icon='check', on_click=self._save_changes).props('flat color=green')
                    ui.button(icon='close', on_click=self._cancel_edit).props('flat color=red')
        
        # Initialize state
        self._toggle_mode(False)

    def _create_view_panel(self):
        """Create read-only view elements"""
        with self.view_panel:
            # Get values with proper defaults
            name = self.task.get('name', '')
            desc = self.task.get('description', '')
            status = self.task.get('is_completed', False)
            created = self.task.get('created_at')
            deadline = self.task.get('updated_at')

            # Create output fields
            with ui.column().classes('w-full gap-4'):
                self.name_view = TextOutput('Task Name', value=name)
                
                # Description with proper multiline support
                self.description_view = TextOutput(
                    'Description',
                    value=desc if desc else '-',
                    multiline=True
                )
                
                # Timestamps section
                with ui.column().classes('gap-2'):
                    self.created_view = DateTimeOutput(
                        'Created',
                        value=created,
                        format='%Y-%m-%d %H:%M'
                    )
                    self.deadline_view = DateTimeOutput(
                        'Deadline',
                        value=deadline,
                        format='%Y-%m-%d %H:%M'
                    )
                
                self.status_view = BooleanOutput('Status', value=status, use_icon=True)

    def _create_edit_panel(self):
        """Create editable input elements"""
        with self.edit_panel:
            self.name_edit = TextInput(
                'Task Name',
                value=self.task.get('name', '')
            )
            self.description_edit = TextInput(
                'Description',
                value=self.task.get('description', ''),
                multiline=True
            )
            self.deadline_edit = DateTimeInput(
                'Deadline',
                value=self.task.get('updated_at'),
                min_date=datetime.now()  # Set current date as minimum
            )

    def _toggle_mode(self, edit_mode: bool):
        """Switch between view and edit modes"""
        self.edit_mode = edit_mode
        self.view_panel.visible = not edit_mode
        self.edit_panel.visible = edit_mode
        self.edit_btn.visible = not edit_mode
        self.action_buttons.visible = edit_mode

    def _start_edit(self):
        """Enter edit mode"""
        self._toggle_mode(True)

    def _save_changes(self):
        """Save changes and exit edit mode"""
        name = self.name_edit.get_value()
        if not name:
            ui.notify('Task name is required', type='negative')
            return
        
        updated_data = {
            'name': name,
            'description': self.description_edit.get_value(),
            'updated_at': self.deadline_edit.get_value()
        }
        
        if self.on_update:
            self.on_update(self.task['id'], updated_data)
            
            # Update view panel values
            self.name_view.set_value(updated_data['name'])
            self.description_view.set_value(updated_data['description'])
            self.deadline_view.set_value(updated_data['updated_at'])
            
        self._toggle_mode(False)

    def _cancel_edit(self):
        """Cancel editing and revert changes"""
        # Reset edit panel values to original
        self.name_edit.set_value(self.task.get('name', ''))
        self.description_edit.set_value(self.task.get('description', ''))
        self.deadline_edit.set_value(self.task.get('updated_at'))
        
        self._toggle_mode(False)
