import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from nicegui import ui
from data.models.task.manager import TaskManager
from data.models.task.validation import TaskQueryParams
from data.base_metadata import Session
from lib.ui.controls.task_item import TaskItemUI
from lib.ui.context.task_filter_context import TaskFilterContext

class TaskListUI:
    def __init__(self, filter_context: TaskFilterContext):
        self.session = Session()
        self.manager = TaskManager(self.session)
        self.container = ui.column().classes('w-full')
        self.filter_context = filter_context
        self.filter_context.subscribe(self.refresh_tasks)

    def delete_task(self, task_id: int):
        response = self.manager.delete_task(task_id)
        if response.status == "success":
            self.refresh_tasks()

    def update_task(self, task_id: int, updated_data: dict):
        """Обновление задачи через менеджер"""
        response = self.manager.update(task_id, **updated_data)
        if response.status == "success":
            self.refresh_tasks()

    def refresh_tasks(self, query_params: TaskQueryParams = None):
        if query_params is None:
            query_params = self.filter_context.current_filter
            
        response = self.manager.get(query_params)
        
        with self.container:
            self.container.clear()
            if response.status == "success":
                for task in response.data:
                    task_dict = task.model_dump()
                    TaskItemUI(
                        task_data=task_dict,
                        on_delete=self.delete_task,
                        on_refresh=lambda: self.refresh_tasks(self.filter_context.current_filter),
                        on_update=self.update_task
                    )

    def create_task(self, task_data: dict):
        """Создание новой задачи"""
        response = self.manager.create(**task_data)
        if response.status == "success":
            self.refresh_tasks()
        else:
            ui.notify(response.message, type='negative')

    def create(self):
        # Remove refresh button and just return container
        return self.container
