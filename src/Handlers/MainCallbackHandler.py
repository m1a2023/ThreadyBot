from telegram import Update
from telegram.ext import ContextTypes
from Handlers.Handler import Handler

""" Импорты хендлеров для главного меню """
from Handlers.MainMenuHandler import MainMenuHandler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from Handlers.HandlersForMainMenu.EventsAndStatusOfProjectHandler import EventsAndStatusOfProjectHandler
from Handlers.HandlersForMainMenu.GeneralSettingsHandler import GeneralSettingsHandler

""" Импорты хендлеров для управления проектами """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.CreateProjectHandler import CreateProjectHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.ChangeProjectHandler import ChangeProjectHandler

""" Импорты хендлеров для создания проекта """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SaveNewProjectHandler import SaveCreateProjectHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetDescriptionHandler import SetDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetNameHandler import SetNameHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetTeamHandler import SetTeamHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetLinkRepHandler import SetLinkRepHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.CancelCreateProjectHandler import CancelCreateProjectHandler

from Handlers.TaskMenu.AddHandler import AddHandler
from Handlers.TaskMenu.EditHandler import EditHandler
from Handlers.TaskMenu.DeleteHandler import DeleteHandler
from Handlers.TaskMenu.ShowHandler import ShowHandler

from Handlers.TaskMenu.AddTaskMenu.NameHandler import NameHandler
from Handlers.TaskMenu.AddTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.TaskMenu.AddTaskMenu.DeadlineHandler import DeadlineHandler
from Handlers.TaskMenu.AddTaskMenu.PriorityHandler import PriorityHandler
from Handlers.TaskMenu.AddTaskMenu.StatusHandler import StatusHandler
from Handlers.TaskMenu.AddTaskMenu.DoneHandler import DoneHandler
from Handlers.TaskMenu.AddTaskMenu.CancelHandler import CancelHandler

from Handlers.TaskMenu.EditTaskMenu.EditDoneHandler import EditDoneHandler

class MainCallbackHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # пока хз, как добавить цикличность
    if query.data == "MoveToMainMenu":
      return await MainMenuHandler.handle(update, context)

    # Обработка кнопок в "Главном меню"
    elif query.data == "SettingsOfProjects":
      return await SettingsOfProjectsHandler.handle(update, context)
    elif query.data == "EventsAndStatusOfProjects":
      return await EventsAndStatusOfProjectHandler.handle(update, context)
    elif query.data == "GeneralSettings":
      return await GeneralSettingsHandler.handle(update, context)

    # Обработка кнопок в "Управление проектами"
    elif query.data == "CreateProject":
      return await CreateProjectHandler.handle(update, context)
    elif query.data == "ChangeProject":
      return await ChangeProjectHandler.handle(update, context)

    # Обработка кнопок в "Создание проекта"
    elif query.data == "setNameForCreateProject":
      return await SetNameHandler.handle(update, context)
    elif query.data == "setDescriptionForCreateProject":
      return await SetDescriptionHandler.handle(update, context)
    elif query.data == "setTeamForCreateProject":
      return await SetTeamHandler.handle(update, context)
    elif query.data == "setLinkForCreateProject":
      return await SetLinkRepHandler.handle(update, context)
    elif query.data == "CancelCreateProject":
      return await CancelCreateProjectHandler.handle(update, context)
    elif query.data == "SaveNewProject":
      return await SaveCreateProjectHandler.handle(update, context)

    #кнопки с задачами
    #кнопки главного меню работы с задачами
    if query.data == "add":
        return await AddHandler.handle(update, context)
    elif query.data == "edit":
        return await EditHandler.handle(update, context)
    elif query.data == "del":
        return await DeleteHandler.handle(update, context)
    elif query.data == "show":
        return await ShowHandler.handle(update, context)
    #кнопки меню добавления задачи
    elif query.data == "name":
        return await NameHandler.handle(update, context)
    elif query.data == "description":
        return await DescriptionHandler.handle(update, context)
    elif query.data == "deadline":
        return await DeadlineHandler.handle(update, context)
    elif query.data == "priority":
        return await PriorityHandler.handle(update, context)
    elif query.data == "status":
        return await StatusHandler.handle(update, context)
    elif query.data == "done":
        return await DoneHandler.handle(update,context)
    elif query.data == "cancel":
        return await CancelHandler.handle(update,context)
    #кнопки меню редактирования задачи
    elif query.data == "edit_done":
        return await EditDoneHandler.handle(update,context)
