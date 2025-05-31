# data/models/task/crud_repository.py
from sqlalchemy.orm import Session, Query

from .model import ModelTask
from .error.not_found_error import NotFoundError

class CRUDTask:

    def __init__(self, session: Session):
        self.session = session
        self.model = ModelTask

    def add(self, task: ModelTask) -> ModelTask:
        try:
            self.session.add(task)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def remove(self, task_id: int) -> bool:
        try:
            task = self.get(task_id)
            self.session.delete(task)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, task_id: int, **kwargs) -> ModelTask:
        try:
            task = self.get(task_id)
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def get(self, task_id: int) -> ModelTask | None:
        """Получить задачу по ID."""
        try:
            task = self.session.get(self.model, task_id)
            if not task:
                raise NotFoundError("Task", task_id)
            return task
        except Exception as e:
            raise e

    def get_all_query(self) -> Query:
        return self.session.query(self.model)
