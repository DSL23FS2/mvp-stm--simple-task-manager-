# data/models/task/manager.py
from sqlalchemy.orm import Query
from sqlalchemy import asc, desc

from .crud_repository import CRUDTask
from .model import ModelTask
from .validation import APIResponse
from .validation import TaskOutput
from .validation import TaskQueryParams
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
                data=[{"task_id": task.id}],
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
                data=[{"task_id": task.id}],
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
                data=[None],
                message="Задача успешно удалена"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e)},
                message="Ошибка при удалении задачи"
            )

    def get_by_id(self, task_id: int):
        try: 
            task = self.crud.get(task_id)
            if not task:
                return format_response(
                    success=False,
                    status_code=404,
                    message="Задача не найдена"
                )
            return APIResponse(
                status="success",
                data=[TaskOutput.model_validate(task)],
                message="Задача получена"
            )
        except Exception as e:
            return format_response(
                success=False,
                status_code=500,
                data={"error": str(e)},
                message="Ошибка при получении задачи по ID"
            )

    def get(self, query_params: TaskQueryParams) -> APIResponse:
        """
        Получить список задач с возможностью фильтрации, сортировки и пагинации.
        :param query_params: Параметры фильтрации и сортировки.
        :return: APIResponse с данными задач.
        """
        
        try:
            query = self.crud.get_all_query()
            query = self._apply_filters(query, query_params)
            query = self._apply_sorting(query, query_params)
            query = self._apply_pagination(query, query_params)
            
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
                data={"error": str(e), "query_params": query_params},
                message="Ошибка при получении задач по фильтрам"
            )

    def _apply_filters(self, query: Query, params: TaskQueryParams) -> Query:
        if params.name:
            query = query.filter(ModelTask.name.ilike(f"%{params.name}%"))
        if params.is_completed is not None:
            query = query.filter(ModelTask.is_completed == params.is_completed)
        return query

    def _apply_sorting(self, query: Query, params: TaskQueryParams) -> Query:
        sort_column = getattr(ModelTask, params.sort_by, None)
        if sort_column is None:
            raise ValueError(f"Недопустимое поле сортировки: {params.sort_by}")
        direction = asc if params.order == "asc" else desc
        return query.order_by(direction(sort_column))

    def _apply_pagination(self, query: Query, params: TaskQueryParams) -> Query:
        return query.offset(params.skip).limit(params.limit)