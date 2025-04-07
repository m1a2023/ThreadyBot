import httpx
from typing import List

from ProjectManagment.Project import Project
from TaskManagement.Task import Task


#
# ЗАПРОСЫ ДЛЯ НАПОМИНАНИЙ
#
async def get_reminders_by_project_ids(project_ids: List[int]):
    async with httpx.AsyncClient() as client:
        ids = "&project_ids=".join(str(project_id) for project_id in project_ids)
        route = "http://localhost:9000/api/db/reminders/bat/?project_ids=" + ids

        response = await client.get(route)
        response.raise_for_status()
        reminders = response.json()

        result = []
        for remind in reminders:
          remind_title = remind.get("title")
          remind_deadline = remind.get("send_time")
          remind_developer = remind.get("user_id")
          project_id = remind.get("project_id")
          task_id = remind.get("task_id")

          remind_info = [remind_title, remind_deadline, remind_developer, project_id, task_id]

          if remind_title and remind_deadline:
              result.append(remind_info)

        return result

async def delete_remind_by_task_id(task_id: int):
   async with httpx.AsyncClient() as client:
     response = await client.delete(f"http://localhost:9000/api/db/reminders/{task_id}")
     response.raise_for_status()

#
# ЗАПРОСЫ ДЛЯ ОТЧЕТОВ
#
async def get_report_by_project_id(project_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:9000/api/db/reports/project/{project_id}")
        response.raise_for_status()
        report = response.json()
        return report

async def get_report_by_user_id(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:9000/api/db/reports/developer/{user_id}")
        response.raise_for_status()
        report = response.json()
        return report

#
# запросы для генерации плана
#
async def get_project_plan(project_id: int, iam_t: str, f_id: str):
    description = "ThreadyServer – это планируемый многопоточный сервер, разработанный на Python с использованием FastAPI. Проект будет включать поддержку асинхронной обработки запросов, работу с базой данных PostgreSQL и удобное API для взаимодействия с клиентами" #await getProjectInfoById(project_id)
    iam_token = iam_t
    folder_id = f"gpt://{f_id}/yandexgpt"

    url = "http://localhost:9000/api/llm/ygpt/"
    params = {
        "url": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        "action": "plan",
        "project_id": project_id,
        "context_depth": 2,
        "timeout" : 60
    }

    body = {
        "iam_token": iam_token,
        "model_uri": folder_id,
        "options": {
            "stream": False,
            "temperature": 0.9,
            "max_tokens": 1200
          },
        "messages": [
          {
                "role": "user",
                "text": description
          }
        ]
      }

    async with httpx.AsyncClient(timeout=30.0) as client:
      #print(description)
      #response = await client.post(f"http://localhost:9000/api/llm/ygpt/?url=https://llm.api.cloud.yandex.net/foundationModels/v1/completion&action=plan&project_id={project_id}&context_depth=2&timeout=60", json=body)
      response = await client.post(
            url=url,
            params=params,
            json=body,
            headers={"Content-Type": "application/json"}
        )
      response.raise_for_status()
      plan = response.json()
      return plan

#
# Запросы для юзеров
#

""" Проверка, есть ли юзер в бд """
async def checkUserExists(user_id: int) -> bool:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/users/{user_id}"
    )
    if response.status_code == 200:
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
      "owner_id": project["owner_id"]
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
      repo_link = data["repo_link"],
    )
    return foundProject

async def getProjectInfoById(project_id) -> Project:
  async with httpx.AsyncClient() as client:
    response = await client.get(
      f"http://localhost:9000/api/db/projects/{project_id}"
    )
    response.raise_for_status()
    data = response.json()
    return data['description']

""" Сохраняет новые данные в проект """
async def updateProjectById(project_id, newInfo: dict):
  async with httpx.AsyncClient() as client:
    try:
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
      response = await client.get(
        f"http://localhost:9000/api/db/teams/project/{project_id}"
      )
      response.raise_for_status()
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
    "title": task.title,
    "description": task.description,
    "deadline": task.deadline.isoformat(),
    "priority": task.priority,
    "status": task.status,
    "project_id": project_id,
    "user_id": task.developer
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
        title = data["title"],
        description = data["description"],
        deadline = data["deadline"],
        priority = data["priority"],
        status = data["status"],
        developer = data["user_id"]
      )

      return task
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")
