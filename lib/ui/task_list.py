from nicegui import ui
from data.models.task.manager import TaskManager
from data.models.task.validation import TaskQueryParams
from data.base_metadata import Session
from .task_item import TaskItemUI

class TaskListUI:
    def __init__(self):
        self.session = Session()
        self.manager = TaskManager(self.session)
        self.container = ui.column().classes('w-full')

    def delete_task(self, task_id: int):
        response = self.manager.delete_task(task_id)
        if response.status == "success":
            self.refresh_tasks()

    def update_task(self, task_id: int, updated_data: dict):
        """Обновление задачи через менеджер"""
        response = self.manager.update(task_id, **updated_data)
        if response.status == "success":
            self.refresh_tasks()

    def refresh_tasks(self):
        query_params = TaskQueryParams()
        response = self.manager.get(query_params)
        
        with self.container:
            self.container.clear()
            
            if response.status == "success":
                for task in response.data:
                    task_dict = task.model_dump()
                    TaskItemUI(
                        task_data=task_dict,
                        on_delete=self.delete_task,
                        on_refresh=self.refresh_tasks,
                        on_update=self.update_task
                    )

    def create(self):
        ui.button('Refresh', on_click=self.refresh_tasks).classes('q-mb-md')
        return self.container
