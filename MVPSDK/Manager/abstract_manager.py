# Абстрактный класс для менеджера, который будет использоваться в других модулях
# и будет реализовывать методы для работы с данными.
# Этот класс будет использоваться в качестве базового класса для конкретных менеджеров,
# которые будут работать с конкретными моделями данных.
# Например, TaskManager будет наследоваться от AbstractManager и реализовывать методы
# для работы с задачами.
# data/core/abstract_manager.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar("T")  # Тип данных (например, Task)

class AbstractManager(ABC, Generic[T]):
    @abstractmethod
    def create(self, model: T):
        """Создает новую запись."""
        pass

    @abstractmethod
    def update(self, id: int, **kwargs):
        """Обновляет по ID."""
        pass

    @abstractmethod
    def delete(self, id: int):
        """Удаляет по ID."""
        pass

    @abstractmethod
    def get(self, filters: dict = None) -> List[T]:
        """Возвращает список с возможностью фильтрации."""
        pass