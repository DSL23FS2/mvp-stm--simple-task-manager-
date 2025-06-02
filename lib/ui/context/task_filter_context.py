from typing import Callable, List
from data.models.task.validation import TaskQueryParams

class TaskFilterContext:
    def __init__(self):
        self._current_filter = TaskQueryParams()
        self._subscribers: List[Callable[[TaskQueryParams], None]] = []

    @property
    def current_filter(self) -> TaskQueryParams:
        return self._current_filter

    def update_filter(self, new_filter: TaskQueryParams):
        self._current_filter = new_filter
        self._notify_subscribers()

    def subscribe(self, callback: Callable[[TaskQueryParams], None]):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def _notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber(self._current_filter)
