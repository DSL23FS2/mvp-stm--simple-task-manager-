# CRUD-репозиторий для работы с базой данных
# Шаблонный класс, который можно использовать для создания CRUD-репозиториев для различных моделей.
# data/core/crud_repository.py

from typing import TypeVar, Generic, Type, List
from sqlalchemy.orm import Session, Query

T = TypeVar("T")  # Тип ORM-модели

class CRUDRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        """
        Универсальный CRUD-репозиторий.
        :param session: Сессия SQLAlchemy.
        :param model: Класс ORM-модели.
        """
        self.session = session
        self.model = model

    def add(self, obj: T) -> T:
        """Добавляет объект в базу данных."""
        self.session.add(obj)
        self.session.commit()
        return obj

    def remove(self, obj_id: int) -> bool:
        """Удаляет объект по ID."""
        obj = self.get(obj_id)
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False;        
        
    def update(self, obj_id: int, **kwargs) -> None:
        """Обновляет объект по ID."""
        try:
            obj = self.get(obj_id)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False

    def get(self, obj_id: int) -> T:
        """Получает объект по ID."""
        obj = self.session.query(self.model).get(obj_id)
        if obj is None:
            raise ValueError(f"Объект с ID {obj_id} не найден.")
        return obj
    
    def get_all_query(self) -> Query:
        """
        Возвращает объект Query для настройки запроса.
        :return: SQLAlchemy Query.
        """
        return self.session.query(self.model)