# data/models/task/crud_repository.py
from .model import ModelTask
from sqlalchemy.orm import Session, Query

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
        task = self.get(task_id)
        if not task:
            return False
        try:
            self.session.delete(task)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, task_id: int, **kwargs) -> ModelTask:
        task = self.get(task_id)
        if not task:
            return None
        try:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def get(self, task_id: int) -> ModelTask | None:
        """Получить задачу по ID."""
        return self.session.get(self.model, task_id)

    def get_all_query(self) -> Query:
        return self.session.query(self.model)
