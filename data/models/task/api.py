# data/models/task/api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from data.base_metadata import get_session
from .manager import TaskManager
from .validation import TaskCreate
from .validation import TaskUpdate
from .validation import APIResponse
from .validation import TaskOutput
from .model import ModelTask

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=APIResponse[List[TaskOutput]])
def get_all_tasks(session: Session = Depends(get_session)):
    """
    Получить список всех задач.
    """
    manager = TaskManager(session)
    return manager.get()
    
@router.get("/{task_id}", response_model=APIResponse[TaskOutput])
def get_task_by_id(task_id: int, session: Session = Depends(get_session)):
    """
    Получить задачу по ID.
    :param task_id: ID задачи.
    """
    manager = TaskManager(session)
    return manager.get([ModelTask.id == task_id])

@router.post("/", response_model=APIResponse[dict])
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    Создать новую задачу.
    :param task: Данные задачи.
    """
    manager = TaskManager(session)
    return manager.create(**task.model_dump())

@router.put("/", response_model=APIResponse[dict])
def update_task(task: TaskUpdate, session: Session = Depends(get_session)):
    """
    Обновить задачу.
    :param task: Данные задачи для обновления.
    """
    manager = TaskManager(session)
    return manager.update(task_id=task.id, **task.model_dump(exclude={"id"}))

@router.delete("/{task_id}", response_model=APIResponse[None])
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """
    Удалить задачу.
    :param task_id: ID задачи для удаления.
    """
    manager = TaskManager(session)
    return manager.delete_task(task_id=task_id)

    # @router.post("/filters")
    # def filter_tasks(filters: TaskFilter):
    #     """
    #     Получить задачи по сложным фильтрам.
    #     :param filters: Условия фильтрации.
    #     """
    #     return manager.get(filters=filters.filters)


