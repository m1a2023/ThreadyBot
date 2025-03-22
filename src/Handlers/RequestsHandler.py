import httpx

from ProjectManagment.Project import Project
from TaskManagement.Task import Task

# 
# Запросы для юзеров
# 

""" Проверка, есть ли юзер в бд """
async def checkUserExists(user_id: int) -> bool:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/users/{user_id}"
    )
    if response.json() is not None:
      return True
    return False

""" Добавление юзера """
async def addNewUser(id, name):
  user_data = {
      "id": id,
      "name": name
  }

  async with httpx.AsyncClient() as client:
      response = await client.post(
          "http://localhost:9000/api/db/users/",
          json=user_data
      )
      response.raise_for_status()
      print("Юзер добалвен")
      return response.json()

async def getUserNameById(user_id: int):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(
        f"http://localhost:9000/api/db/users/{user_id}"  # URL эндпоинта
      )
      response.raise_for_status()
      user_data = response.json()
      return user_data.get("name")
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")


# 
# Запросы для проектов
# 

""" Запрос для сохранения проекта в бд """
async def saveNewProject(project):
  project_data = {
      "title": project["title"],
      "description": project["description"],
      "repo_link": project["repo_link"],
      "owner_id": int(project["owner_id"]),
  }
  
  async with httpx.AsyncClient() as client:
      response = await client.post(
          "http://localhost:9000/api/db/projects/",
          json=project_data
      )
      response.raise_for_status()
      print("Проект успешно создан! ID проекта:", response.json())
      return response.json()

""" Запрос для получения всех проектов конкретного челика. Возвращает список словарей со всеми данными"""
async def getAllProjects(owner_id) -> list:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/projects/owner/{owner_id}"
    )
    response.raise_for_status()
    projects = response.json()
    return projects

""" Возвращает данные о проекте по его id """
async def getProjectById(project_id) -> Project:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/projects/{project_id}"
    )
    response.raise_for_status()
    data = response.json()
    foundProject = Project(
      title = data["title"], 
      description = data["description"], 
      repo_link = data["repo_link"]
    )
    return foundProject
  
""" Сохраняет новые данные в проект """
async def updateProjectById(project_id, newInfo: dict):
  async with httpx.AsyncClient() as client:
    try:
      # Отправляем PUT-запрос
      response = await client.put(
        f"http://localhost:9000/api/db/projects/{project_id}",
        json=newInfo
      )
      response.raise_for_status()
      return response
    except httpx.HTTPStatusError as e:
      print(f"Ошибка HTTP: {e}")
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Удаляет проект по ID """
async def deleteProject(project_id: int):
  async with httpx.AsyncClient() as client:
    try:
      # Отправляем DELETE-запрос
      response = await client.delete(
        f"http://localhost:9000/api/db/projects/{project_id}"
      )
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

# 
# Запросы для тимы
# 

""" Запрос для создания тимы """
async def createNewTeams(team_data: dict):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.post(
        "http://localhost:9000/api/db/teams/",
        json=team_data
      )
      response.raise_for_status() 
      return response.json()  
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")
  
""" Запрос на добавление нового человека в команду """
async def addUserToTeam(team_data: dict):
  async with httpx.AsyncClient() as client:
    try:
      # Отправляем POST-запрос
      response = await client.post(
        "http://localhost:9000/api/db/teams/user", 
        json=team_data
      )
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Удаление юзера из команды """
async def deleteUserFromTeam(user_id: int, project_id: int):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.delete(
        f"http://localhost:9000/api/db/teams/user/{user_id}/project/{project_id}"
      )
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Запрос на получение команды """
async def getTeamByProjectId(project_id: int):
  async with httpx.AsyncClient() as client:
    try:
      # Отправляем GET-запрос
      response = await client.get(
        f"http://localhost:9000/api/db/teams/project/{project_id}"  # URL эндпоинта
      )
      response.raise_for_status()  # Проверяем на ошибки HTTP
      return response.json()
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Запрос на получение команды, возвращающий только id разработчиков """
async def getListDevelopersIdByProjectId(project_id: int):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(
        f"http://localhost:9000/api/db/teams/project/{project_id}"
      )
      response.raise_for_status()

      data = response.json()

      # Извлекаем список ID разработчиков
      developers_id = []
      for item in data:
        developers_id.append(item["user_id"])
      
      return developers_id
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

# 
# Запросы для тасков
# 

""" Создает задачу """
async def createTask(task: Task, project_id: int):
  task_data = {
    "title": task._name,
    "description": task._description,
    "deadline": task._deadline.isoformat(),
    "priority": task._priority,
    "status": task._status,
    "project_id": project_id
  }
  async with httpx.AsyncClient() as client:
    try:
      response = await client.post(
        "http://localhost:9000/api/db/tasks/", 
        json=task_data
      )

      response.raise_for_status() 
      return response.json()  
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Запрос на редактирование задачи """
async def updateTaskById(task_id, newInfo: dict):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.put(
        f"http://localhost:9000/api/db/tasks/{task_id}",
        json=newInfo
      )
      response.raise_for_status()
      return response
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Запрос на вывод всех задач по id проекта """
async def getAllTasks(project_id) -> list:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/tasks/project/{project_id}"
    )
    response.raise_for_status()
    tasks = response.json()
    return tasks
  
""" Запрос на удаление задачи """
async def deleteTaskById(task_id: int):
  async with httpx.AsyncClient() as client:
    try:
      response = await client.delete(
        f"http://localhost:9000/api/db/tasks/{task_id}"
      )
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")

""" Запрос на получение данных о задаче """
async def getTaskById(task_id: int) -> Task:
  async with httpx.AsyncClient() as client:
    try:
      response = await client.get(
        f"http://localhost:9000/api/db/tasks/{task_id}"
      )
      response.raise_for_status()
      data = response.json()
      
      task = Task(
        _name = data["title"], 
        _description = data["description"], 
        _deadline = data["deadline"],
        _priority = data["priority"],
        _status = data["status"]
      )

      return task
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")