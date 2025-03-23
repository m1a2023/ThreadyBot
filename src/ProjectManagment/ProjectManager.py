from telegram import Update
from telegram.ext import ContextTypes

class ProjectManager():
    PROJECTS = []

    @staticmethod
    async def add_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
        ProjectManager.PROJECTS.append(context.user_data["project"])

    @staticmethod
    async def edit_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("отредвчен проект")

    @staticmethod
    async def delete_project(project_name,update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_to_delete = ProjectManager.found_project(project_name, update, context)

        if proj_to_delete:
            ProjectManager.PROJECTS.remove(proj_to_delete)
            response_text = f"Проект '{project_name}' удален."
        else:
            response_text = f"Проект '{project_name}' не найден."
        return response_text

    @staticmethod
    async def get_projects():
        print("from get projs")
        if not ProjectManager.PROJECTS:
            return "Список проектов пуст."

        return "\n---\n".join([f"{i + 1}. {proj}" for i, proj in enumerate(ProjectManager.PROJECTS)])

    @staticmethod
    async def show_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("from show projs")
        projs_text = await ProjectManager.get_projects()

        if update.message:
            await update.message.reply_text(projs_text)
        elif update.callback_query:
            await update.callback_query.message.reply_text(projs_text)

    @staticmethod
    def found_project(proj_name,update: Update, context: ContextTypes.DEFAULT_TYPE):
        return next((proj for proj in context.user_data["project_manager"].PROJECTS if proj.name == proj_name), None)

    async def get_projects_list():
        print("from get projs list")
        if not ProjectManager.PROJECTS:
            return "Список проектов пуст."

        return [(i+1,proj) for i, proj in enumerate(ProjectManager.PROJECTS)]