import uuid
from datetime import datetime,timezone


from Enums import Priority, Status

class Task():

    def __init__(self, id,
                 name,
                 description,
                 deadline=None,
                 priority: Priority=None,
                 status: Status=None):

        #self.id = str(uuid.uuid4())
        self._name = name
        self._description = description
        #self._deadline = datetime.strptime(deadline, "%Y-%m-%d") #TODO timezone utc
        self._priority = priority
        self._status = status

    def edit_task(self, name=None, description=None, deadline=None, priority=None, status=None):
            if name:
                self.name = name
            if description:
                self.description = description
            if deadline:
                self.deadline = datetime.strptime(deadline, "%Y-%m-%d") #TODO timezone utc
            if priority:
                self.priority = priority
            if status:
                self.status = status

    """def edit_name(self, name) -> None:
        self._name = name

    def edit_description(self, description) -> None:
        self._description = description

    def edit_deadline(self, deadline) -> None:
        self._deadline = datetime.strptime(deadline, "%Y-%m-%d")

    def edit_deadline(self, priority: Priority) -> None:
        self._priority = priority

    def edit_status(self, status: Status) -> None:
        self._status = status"""


    """def __str__(self):
        return (f"Name: {self._name}\nDescription: {self._description}\nDeadline: {self._deadline}\nPriority: {self._priority}\nStatus: {self._status}")
"""
