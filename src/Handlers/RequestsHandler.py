import httpx

from ProjectManagment.Project import Project

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
      # Проверка статуса ответа
      response.raise_for_status()
      print("Юзер добалвен")
      return response.json()

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
    data = response.json() #Словарь с данными
    foundProject = Project(
      title = data["title"], 
      description = data["description"], 
      repo_link = data["repo_link"]
    )
    return foundProject
  

async def updateProjectById(project_id, newInfo: dict):
  async with httpx.AsyncClient() as client:
    try:
      # Отправляем PUT-запрос
      response = await client.put(
        f"http://localhost:9000/api/db/projects/{project_id}",
        json=newInfo
      )
      response.raise_for_status()  # Проверяем на ошибки HTTP
      return response  # Возвращаем ID обновленного проекта
    except httpx.HTTPStatusError as e:
      print(f"Ошибка HTTP: {e}")
    except Exception as e:
      print(f"Неожиданная ошибка: {e}")
