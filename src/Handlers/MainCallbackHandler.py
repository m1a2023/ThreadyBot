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

""" Импорты хендлеров для изменения данных уже существующих проектов """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.ChangeInfoAboutTeamHandler import ChangeInfoAboutTeamHandler

""" Импорты хендлеров для изменения тимы """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.HandlersForChangeInfoAboutTeam.AddNewDeveloperHandler import AddNewDeveloperHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.HandlersForChangeInfoAboutTeam.DeleteDeveloperHandler import DeleteDeveloperHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.HandlersForChangeInfoAboutTeam.CancelChangeTeamHandler import CancelChangeTeamHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.HandlersForChangeInfoAboutTeam.SaveChangeTeamHandler import SaveChangeTeamHandler

""" Импорты хендлеров для создания проекта """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SaveNewProjectHandler import SaveCreateProjectHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetDescriptionHandler import SetDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetNameHandler import SetNameHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetTeamHandler import SetTeamHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetLinkRepHandler import SetLinkRepHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.CancelCreateProjectHandler import CancelCreateProjectHandler

""" Импорты хендлеров для тасков """
from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler

from Handlers.HandlersForTaskMenu.AddHandler import AddHandler
from Handlers.HandlersForTaskMenu.EditHandler import EditHandler
from Handlers.HandlersForTaskMenu.DeleteHandler import DeleteHandler
from Handlers.HandlersForTaskMenu.ShowHandler import ShowHandler
from Handlers.HandlersForTaskMenu.CancelTaskMenuHandler import CancelTaskMenuHandler

from Handlers.HandlersForTaskMenu.AddNewTaskMenu.NameHandler import NameHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.DeadlineHandler import DeadlineHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.PriorityHandler import PriorityHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.StatusHandler import StatusHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.DoneHandler import DoneHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.CancelHandler import CancelHandler

from Handlers.HandlersForTaskMenu.EditTaskMenu.EditDoneHandler import EditDoneHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditDescriptionHandler import EditDescriptionHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditDeadlineHandler import EditDeadlineHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditPriorityHandler import EditPriorityHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditNameHandler import EditNameHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditStatusHandler import EditStatusHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.CancelEditTaskHandler import CancelEditTaskHandler

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

    # Обработка кнопок в ""Изменить сущестсвующий проект""
    elif query.data == "changeTasks":
       return await MainTaskMenuHandler.handle(update, context)
    elif query.data == "changeTeam":
       return await ChangeInfoAboutTeamHandler.handle(update, context)
    
    # Обработка кнопок в "Изменение данных о команде"
    elif query.data == "addNewDeveloper":
       return await AddNewDeveloperHandler.handle(update, context)
    elif query.data == "deleteDeveloper":
      return await DeleteDeveloperHandler.handle(update, context)
    elif query.data == "cancelChangeTeam":
      return await CancelChangeTeamHandler.handle(update, context)
    elif query.data == "saveChangeTeam":
      return await SaveChangeTeamHandler.handle(update, context)

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
    elif query.data == "cancelTaskMenu":
        return await CancelTaskMenuHandler.handle(update, context)
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

    elif query.data == "editTaskName":
       return await EditNameHandler.handle(update,context)
    elif query.data == "editTaskDescription":
       return await EditDescriptionHandler.handle(update, context)
    elif query.data == "editTaskDeadline":
       return await EditDeadlineHandler.handle(update, context)
    elif query.data == "editTaskPriority":
       return await EditPriorityHandler.handle(update, context)
    elif query.data == "editTaskStatus":
       return await EditStatusHandler.handle(update, context)
    elif query.data == "edit_done":
        return await EditDoneHandler.handle(update,context)
    elif query.data == "edit_cancel":
        return await CancelEditTaskHandler.handle(update,context)
