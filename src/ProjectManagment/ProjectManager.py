from telegram import Update
from telegram.ext import ContextTypes

from Handlers.RequestsHandler import getAllProjects

class ProjectManager:
    def __init__(self):
        self.projects = []

    async def add_project(self, project):
        self.projects.append(project)
        print(f"Проект '{project.name}' добавлен для владельца {self.owner_id}.")

    @staticmethod
    async def get_and_update_list_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "project_manager" not in context.user_data:
            context.user_data["project_manager"] = ProjectManager()
        if update.message:
            context.user_data["project_manager"].projects = await getAllProjects(update.message.from_user.id)
        else:
            context.user_data["project_manager"].projects = await getAllProjects(update.callback_query.from_user.id)

    # async def edit_project(self, project_name, new_project_data):
    #     project = self.found_project(project_name)
    #     if project:
    #         project.update(new_project_data)
    #         print(f"Проект '{project_name}' отредактирован.")
    #     else:
    #         print(f"Проект '{project_name}' не найден.")

    async def delete_project(self, project_name):
        project = self.found_project(project_name)
        if project:
            self.projects.remove(project)
            response_text = f"Проект '{project_name}' удален."
        else:
            response_text = f"Проект '{project_name}' не найден."
        return response_text

    async def get_projects_names_and_id(self): # Вернет список с именами проектов
        list_of_projects = []
        if not self.projects:
           return []
        for project in self.projects:
            list_of_projects.append((project["title"], project["id"]))
        return list_of_projects

    def found_project(self, project_name):
        return next((proj for proj in self.projects if proj.name == project_name), None)