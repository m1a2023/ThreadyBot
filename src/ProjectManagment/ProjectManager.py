from telegram import Update
from telegram.ext import ContextTypes

from Handlers.RequestsHandler import getAllProjectsByOwnerId

class ProjectManager:
    def __init__(self):
        self.projects = []

    # async def add_project(self, project):
    #     self.projects.append(project)
    #     print(f"Проект '{project.name}' добавлен для владельца {self.owner_id}.")

    @staticmethod
    async def get_and_update_list_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "project_manager" not in context.user_data:
            context.user_data["project_manager"] = ProjectManager()
        if update.message:
            context.user_data["project_manager"].projects = await getAllProjectsByOwnerId(update.message.from_user.id)
        else:
            context.user_data["project_manager"].projects = await getAllProjectsByOwnerId(update.callback_query.from_user.id)

    async def get_projects_names_and_id(self): # Вернет список кортежей, с именами проектов и их id
        list_of_projects = []
        if not self.projects:
           return []
        for project in self.projects:
            list_of_projects.append((project["title"], project["id"]))
        return list_of_projects
    
    async def get_projects_names_and_id_from_list(projects_id: list): # Вернет список кортежей, с именами проектов и их id
        list_of_projects = []
        if not projects_id:
           return []
        for project in projects_id:
            list_of_projects.append((project["title"], project["id"]))
        return list_of_projects
    
    async def get_projects_names(self): # Вернет список с именами проектов
        list_of_projects = []
        if not self.projects:
           return []
        for project in self.projects:
            list_of_projects.append(project["title"])
        return list_of_projects
