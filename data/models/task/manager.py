from fastapi import HTTPException
from fastapi.responses import JSONResponse
from MVPSDK.Interface import model_to_dict_list

from .crud_repository import CRUDTask
from .model import ModelTask
from .api_validation import TaskOutput

class TaskManager:
    
    def __init__(self, session):
        """
        Менеджер для работы с задачами.
        :param session: Сессия SQLAlchemy.
        """
        self.crud = CRUDTask(session)
        self.key = [key for key in ModelTask.__table__.columns.keys()]

    def create(self, **kwargs) -> ModelTask:
        """Создает новую задачу."""
        
        for key, value in kwargs.items():  # Исправлено
            if key not in self.key:
                raise HTTPException(
                    status_code=400,
                    detail=f"Такого поля в задаче не существует: {key}"
                )
        
        task = ModelTask(**kwargs)
        return self.crud.add(task=task)

    def update(self, task_id: int, **kwargs) -> bool:
        """Обновляет задачу по ID."""
        return self.crud.update(task_id, **kwargs)

    def delete_task(self, task_id: int) -> bool:
        """Удаляет задачу по ID."""
        return self.crud.remove(task_id)

    def get(self, filters: dict = None) -> list[ModelTask]:
        """Возвращает список задач с возможностью фильтрации."""
        try:                 
            query = self.crud.get_all_query()
            if filters:
                for condition in filters:
                    query = query.filter(condition)
            tasks = [TaskOutput.model_validate(task) for task in query.all()]
            return tasks
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении задач: {str(e)} с фильтрами {filters}"
            )