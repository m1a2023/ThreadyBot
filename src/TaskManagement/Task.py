import uuid
from datetime import datetime, timezone
from Enums.Priority import Priority
from Enums.Status import Status

class Task:
    def __init__(self):
        self._name = None
        self._description = None
        self._deadline = None
        self._priority = None
        self._status = None

    def set_name(self,task_name):
        self._name = task_name

    def set_description(self,task_description):
        self._description = task_description

    def set_deadline(self,task_deadline):
        if task_deadline:
            self._deadline = datetime.strptime(task_deadline, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        else:
            self._deadline = None

    def set_priority(self,task_priority:str):
        if task_priority.lower() == "low":
            self._priority = Priority.LOW
        if task_priority.lower() == "medium":
            self._priority = Priority.MEDIUM
        if task_priority.lower() == "high":
            self._priority = Priority.HIGH

    def set_status(self,task_status:str):
        if task_status.lower() == "todo":
            self._status = Status.TODO
        if task_status.lower() == "in progress":
            self._status = Status.IN_PROGRESS
        if task_status.lower() == "done":
            self._status = Status.DONE

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

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "description": self._description,
            "deadline:": self._deadline,
            "prioritet:": self._priority,
            "status:": self._status
        }
