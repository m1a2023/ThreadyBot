import uuid
from datetime import datetime, timezone
from Enums.Priority import Priority
from Enums.Status import Status

class Task:
    def __init__(self, name, description, deadline=None, priority: Priority = None, status: Status = None):
        self._name = name
        self._description = description
        """self._priority = priority
        self._status = status"""

        if priority == "low":
            self._priority = Priority.LOW
        if priority == "medium":
            self._priority = Priority.MEDIUM
        if priority == "high":
            self._priority = Priority.HIGH
        if status == "todo":
            self._status = Status.TODO
        if status == "in progress":
            self._status = Status.IN_PROGRESS
        if status == "done":
            self._status = Status.DONE

        if deadline:
            self._deadline = datetime.strptime(deadline, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        else:
            self._deadline = None

    def __str__(self):
        return (f"Задача: {self._name}\n"
                f"Описание: {self._description}\n"
                f"Дедлайн: {self._deadline if self._deadline else 'Не установлен'}\n"
                f"Приоритет: {self._priority if self._priority else 'Не указан'}\n"
                f"Статус: {self._status if self._status else 'Не указан'}")

    def edit_task(self, name=None, description=None, deadline=None, priority=None, status=None):
        if name:
            self._name = name
        if description:
            self._description = description
        if deadline:
            self._deadline = datetime.strptime(deadline, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if priority == "low":
            self._priority = Priority.LOW
        if priority == "medium":
            self._priority = Priority.MEDIUM
        if priority == "high":
            self._priority = Priority.HIGH
        if status == "todo":
            self._status = Status.TODO
        if status == "in progress":
            self._status = Status.IN_PROGRESS
        if status == "done":
            self._status = Status.DONE
