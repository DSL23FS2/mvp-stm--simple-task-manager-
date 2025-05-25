from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

from .manager import TaskManager
from .api_validation import TaskCreate, TaskUpdate, TaskDelete, TaskFilter
from .model import ModelTask

def route_api(session: sessionmaker) -> APIRouter:
    """
    Функция для создания маршрутов API для задач.
    :param session: Сессия SQLAlchemy.
    :return: APIRouter с маршрутами для задач.
    """
    
    router = APIRouter(prefix="/tasks", tags=["tasks"])
    manager = TaskManager(session);
    
    @router.get("/")
    def get_tasks():
        """
        Получить список всех задач.
        """
        return manager.get()
        
    @router.get("/{task_id}")
    def get_tasks(task_id: int):
        """
        Получить задачу по ID.
        :param task_id: ID задачи.
        """
        return manager.get([ModelTask.id == task_id])

    @router.post("/create")
    def create_task(task: TaskCreate):
        """
        Создать новую задачу.
        :param task: Данные задачи.
        """
        return manager.create(**task.model_dump(exclude={"id"}))

    @router.put("/update")
    def update_task(task: TaskUpdate):
        """
        Обновить задачу.
        :param task: Данные задачи для обновления.
        """
        return manager.update(task_id=task.id, **task.model_dump(exclude={"id"}))

    @router.delete("/{task_id}")
    def delete_task(task_id: int):
        """
        Удалить задачу.
        :param task_id: ID задачи для удаления.
        """
        return manager.delete_task(task_id=task_id)

    # @router.post("/filters")
    # def filter_tasks(filters: TaskFilter):
    #     """
    #     Получить задачи по сложным фильтрам.
    #     :param filters: Условия фильтрации.
    #     """
    #     return manager.get(filters=filters.filters)


    return router
