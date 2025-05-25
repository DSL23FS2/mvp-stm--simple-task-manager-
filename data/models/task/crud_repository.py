from .model import ModelTask
from sqlalchemy.orm import Session, Query
from fastapi.responses import JSONResponse
from fastapi import HTTPException
class CRUDTask:
    
    def __init__(self, session: Session):
        """
        CRUD-репозиторий для работы с задачами.
        :param session: Сессия SQLAlchemy.
        """
        self.session = session
        self.model = ModelTask
        
    def add(self, task: ModelTask) -> ModelTask:
        """Добавляет задачу в базу данных."""
        try:
            self.session.add(task)
            self.session.commit()
            return JSONResponse(
                status_code=201,
                content={"message": "Задача успешно добавлена", "task_id": task.id}
            )
        except Exception as e: 
            self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при добавлении задачи: {str(e)}"
            )
        
    def remove(self, task_id: int) -> bool:
        """Удаляет задачу по ID."""
        task = self.get(task_id)
        if not task:
            return False
        try:
            self.session.delete(task)
            self.session.commit()
            return JSONResponse(
                status_code=200,
                content={"message": "Задача успешно удалена"}
            )
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при удалении задачи: {str(e)}"
            )
    
    def update(self, task_id: int, **kwargs) -> bool:
        """Обновляет задачу по ID."""
        task = self.get(task_id)
        if not task:
            return False
        try:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.session.commit()
            return JSONResponse(
                status_code=200,
                content={"message": "Задача успешно обновлена"}
            )
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при обновлении задачи: {str(e)}"
            )
        
    def get(self, task_id: int) -> ModelTask:
        """Получает задачу по ID."""
        task = self.session.query(self.model).get(task_id)
        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Задача с ID {task_id} не найдена."
            )
        return task
    
    def get_all_query(self) -> Query:
        """Возвращает объект Query для настройки запроса."""
        return self.session.query(self.model)