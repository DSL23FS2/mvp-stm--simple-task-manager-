# data/models/task/manager.py
from .crud_repository import CRUDTask
from .model import ModelTask
from .validation.response import APIResponse
from .validation.taskoutput import TaskOutput
from MVPSDK.format_response import format_response


class TaskManager:

    def __init__(self, session):
        self.crud = CRUDTask(session)
        self.key = [key for key in ModelTask.__table__.columns.keys()]

    def create(self, **kwargs):
        for key in kwargs:
            if key not in self.key:
                return format_response(
                    success=False,
                    status_code=400,
                    data={"error": f"Invalid field: {key}"},
                    message="Ошибка валидации данных"
                )
        try:
            task = ModelTask(**kwargs)
            task = self.crud.add(task)
            return APIResponse(
                status="success",
                data={"task_id": task.id},
                message="Задача успешно добавлена"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e)},
                message="Ошибка при добавлении задачи"
            )

    def update(self, task_id: int, **kwargs):
        try:
            task = self.crud.update(task_id, **kwargs)
            if not task:
                return format_response(
                    success=False,
                    status_code=404,
                    message="Задача не найдена"
                )
            return APIResponse(
                status="success",
                data={"task_id": task.id},
                message="Задача успешно обновлена"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e)},
                message="Ошибка при обновлении задачи"
            )

    def delete_task(self, task_id: int):
        try:
            result = self.crud.remove(task_id)
            if not result:
                return format_response(
                    success=False,
                    status_code=404,
                    message="Задача не найдена"
                )
            return APIResponse(
                status="success",
                data=None,
                message="Задача успешно удалена"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e)},
                message="Ошибка при удалении задачи"
            )

    def get(self, filters: dict = None):
        try:
            query = self.crud.get_all_query()
            if filters:
                for condition in filters:
                    query = query.filter(condition)
            tasks = [
                TaskOutput.model_validate(task)
                for task in query.all()
            ]
            return APIResponse(
                status="success",
                data=tasks,
                message="Список задач получен"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e), "filters": filters},
                message="Ошибка при получении задач"
            )
