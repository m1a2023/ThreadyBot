import uuid
from datetime import datetime, timezone
from Enums.Priority import Priority
from Enums.Status import Status

class Task:
    def __init__(self, title: str = None, description = None, deadline = None, priority = None, status = None, executor = None):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.executor = executor

    def set_title(self,task_name):
        self.title = task_name

    def set_description(self,task_description):
        self.description = task_description

    def set_deadline(self,task_deadline):
        if task_deadline:
            self.deadline = datetime.strptime(task_deadline, "%Y-%m-%d")
        else:
            self.deadline = None

    def set_priority(self, task_priority:str):
        self.priority = task_priority

    def set_status(self,task_status:str):
        self.status = task_status
    
    def set_executor(self,task_executor:str):
        self.executor = task_executor

    def __str__(self):
        return (f"Задача: {self.title}\n"
                f"Описание: {self.description}\n"
                f"Дедлайн: {self.deadline if self.deadline else 'Не установлен'}\n"
                f"Приоритет: {self.priority if self.priority else 'Не указан'}\n"
                f"Статус: {self.status if self.status else 'Не указан'}\n"
                f"Исполнитель: {self.executor if self.executor else 'Не указан'}")

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status,
            "user_id": self.executor
        }
