import uuid
from datetime import datetime, timezone
from Enums.Priority import Priority
from Enums.Status import Status

class Task:
    def __init__(self, _name: str = None, _description = None, _deadline = None, _priority = None, _status = None):
        self._name = _name
        self._description = _description
        self._deadline = _deadline
        self._priority = _priority
        self._status = _status

    def set_name(self,task_name):
        self._name = task_name

    def set_description(self,task_description):
        self._description = task_description

    def set_deadline(self,task_deadline):
        if task_deadline:
            self._deadline = datetime.strptime(task_deadline, "%Y-%m-%d")
        else:
            self._deadline = None

    def set_priority(self, task_priority:str):
        self._priority = task_priority

    def set_status(self,task_status:str):
        self._status = task_status

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
    
    def __str__(self):
        deadline_str = (
            datetime.fromisoformat(self._deadline).strftime("%d.%m.%Y")
            if self._deadline
            else "Нет дедлайна"
        )

        # Форматируем строку с информацией о задаче
        return (
            f"Задача: {self._name}\n"
            f"Описание: {self._description}\n"
            f"Статус: {self._status}\n"
            f"Приоритет: {self._priority}\n"
            f"Дедлайн: {deadline_str}"
        )
