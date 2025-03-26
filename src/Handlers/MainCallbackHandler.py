from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.CurrentTasksHandler import CurrentTasksHandler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForCurrentTask.FastEditTaskForStatusDone import FastEditTaskForStatusDone
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForCurrentTask.FastEditTaskForStatusInProgress import FastEditTaskForStatusInProgress
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForCurrentTask.ShowInfoAndFastEditTasksHandler import ShowInfoAndFastEditTasksHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetDeveloperForCreateHandler import SetDeveloperForTaskHandler
from Handlers.HandlersForTaskMenu.ChooseDeveloperHandler import ChooseDeveloperHandler
from Handlers.HandlersForTaskMenu.ChooseTaskHandler import ChooseTaskHandler
from Handlers.HandlersForTaskMenu.ConfirmationDeleteTask import ConfirmationDeleteTaskHandler
from Handlers.HandlersForTaskMenu.DeleteTaskHandler import DeleteTaskHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditDeveloperHandler import EditDeveloperForTaskHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditTaskMenuHandler import EditTaskMenuHandler
from Handlers.TextHandler import TextHandler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForGeneratingProjectPlan.SaveGeneratedPlanHandler import SaveGeneratedPlanHandler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForGeneratingProjectPlan.ShowCurrentPlanHandler import ShowCurrentPlanHandler

""" Импорты хендлеров для главного меню """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.DeleteProjectHandler import DeleteProjectHandler
from Handlers.MainMenuHandler import MainMenuHandler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from Handlers.HandlersForMainMenu.EventsAndStatusOfProjectHandler import EventsAndStatusOfProjectHandler
from Handlers.HandlersForMainMenu.GeneralSettingsHandler import GeneralSettingsHandler

""" Импорты хендлеров для ближайших событий и состояния проекта """
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.ReportHandler import ReportMenuHandler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.ProjectReportHandler import ProjectReportHandler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.UserReportHandler import UserReportHandler

"""для генерации плана"""
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.GeneratePlanHandler import GeneratePlanHandler

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
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.ChooseProjectHandler import ChooseProjectHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.ShowProjectsInfoHandler import ShowProjectsInfoHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.ConfirmationDeleteProjectHandler import ConfirmationDeleteProjectHandler

""" Импорты хендлеров для создания проекта """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SaveNewProjectHandler import SaveCreateProjectHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetDescriptionHandler import SetDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetNameHandler import SetNameHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetTeamHandler import SetTeamHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetLinkRepHandler import SetLinkRepHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.CancelCreateProjectHandler import CancelCreateProjectHandler

""" Импорты хендлеров для редактирования проекта """
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForChangeProject.EditProjectInfoHandler import EditProjectInfoHandler

from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectNameHandler import EditProjectNameHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectDescriptionHandler import EditProjectDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectRepoLinkHandler import EditProjectRepoLinkHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectTeamHandler import EditProjectTeamHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.SaveProjectChangesHandler import SaveProjectChangesHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.CancelEditProjectHandler import CancelEditProjectHandler

from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler

from Handlers.HandlersForTaskMenu.CreateNewTaskHandler import CreateNewTaskHandler
from Handlers.HandlersForTaskMenu.ShowAllTaskHandler import ShowAllTaskHandler

from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetNameHandler import SetNameTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetDescriptionForCreateTaskHandler import SetDescriptionForCreateTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetDeadlineForCreateTaskHandler import SetDeadlineForCreateTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetPriorityForTaskHandler import SetPriorityForTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetStatusForCreateTaskHandler import SetStatusForCreateTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SaveCreateTaskHandler import SaveCreateTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.CancelCreateTaskHandler import CancelCreateTaskHandler

from Handlers.HandlersForTaskMenu.EditTaskMenu.SaveEditTaskHandler import SaveEditTaskHandler
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

    if query.data == "MoveToMainMenu":
      return await MainMenuHandler.handle(update, context)

    # Обработка кнопок в "Главном меню"
    elif query.data == "SettingsOfProjects":
      return await SettingsOfProjectsHandler.handle(update, context)
    elif query.data == "EventsAndStatusOfProjects":
      return await EventsAndStatusOfProjectHandler.handle(update, context)
    elif query.data == "GeneralSettings":
      return await GeneralSettingsHandler.handle(update, context)

    # Обработка кнопок в "Ближайшие события и состояние проекта"
    elif query.data == "currentTasks":
      context.user_data["state"] = "currentTasks"
      return await ChooseProjectHandler.handle(update, context)

    elif query.data == "FastEditTaskForStatusDone":
      return await FastEditTaskForStatusDone.handle(update, context)
    elif query.data == "FastEditTaskForStatusInProgress":
      return await FastEditTaskForStatusInProgress.handle(update, context)

    elif query.data == "reportsMenu":
      return await ReportMenuHandler.handle(update, context)
    elif query.data == "get_project_report":
      context.user_data["state"] = "get_project_report"
      return await ChooseProjectHandler.handle(update, context)
    elif query.data == "get_developer_report":
      context.user_data["state"] = "chooseDeveloper"
      return await ChooseProjectHandler.handle(update, context)
    elif query.data.startswith("taskInCurrentTasks_"):
      context.user_data["taskInCurrentTasks"] = query.data[19:]
      return await ShowInfoAndFastEditTasksHandler.handle(update, context)

    #генерация плана проекта
    elif query.data == "Plan":
      context.user_data["state"] = "PLan"
      return await ChooseProjectHandler.handle(update, context)


    #elif query.data == "generate_menu":
    #   return await GeneratingPlanMenuHandler.handle(update, context)

    # Обработка кнопок с генерацией плана
    elif query.data == "save_generated_plan":
      return await SaveGeneratedPlanHandler.handle(update, context)
    elif query.data == "show_current_plan":
      return await ShowCurrentPlanHandler.handle(update, context)
    #elif query.data == "generate_plan":
    #  return await GenerateProjectPlanHandler.handle(update, context)

    # Обработка кнопок в "Управление проектами"
    elif query.data == "CreateProject":
      return await CreateProjectHandler.handle(update, context)

    elif query.data == "ChangeProject":
      context.user_data["state"] = "changeProject"
      return await ChooseProjectHandler.handle(update, context)

    elif query.data == "ShowProjectsInfo":
      context.user_data["state"] = "showProjectsInfo"
      return await ChooseProjectHandler.handle(update, context)

    elif query.data == "ConfirmationDeleteProject":
      context.user_data["state"] = "deleteProject"
      return await ChooseProjectHandler.handle(update, context)

    elif query.data == "deleteProject":
      return await DeleteProjectHandler.handle(update, context)

    elif query.data == "deleteTask":
      return await DeleteTaskHandler.handle(update, context)

    #кнопка изменения задач (в меню изменения проекта)
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

    # Обработка кнопок в "Изменении проекта"
    elif query.data == "editProject":
      return await EditProjectInfoHandler.handle(update, context)

    elif query.data == "changeNameProject":
      return await EditProjectNameHandler.handle(update, context)
    elif query.data == "changeDescriptionProject":
      return await EditProjectDescriptionHandler.handle(update, context)
    elif query.data == "changeLinkProject":
      return await EditProjectRepoLinkHandler.handle(update, context)
    elif query.data == "saveProjectChanges":
      return await SaveProjectChangesHandler.handle(update, context)
    elif query.data == "cancelProjectEdit":
      return await CancelEditProjectHandler.handle(update, context)

    #кнопки с задачами
    #кнопки главного меню работы с задачами
    if query.data == "createNewTask":
      return await CreateNewTaskHandler.handle(update, context)
    elif query.data == "editTask":
      context.user_data["state"] = "editTask"
      return await ChooseTaskHandler.handle(update, context)

    elif query.data == "confirmationDeleteTask":
      context.user_data["state"] = "deleteTask"
      return await ChooseTaskHandler.handle(update, context)
    elif query.data == "deleteTask":
      context.user_data["state"] = "deleteTask"
      return await ChooseTaskHandler.handle(update, context)
    elif query.data == "showTask":
      return await ShowAllTaskHandler.handle(update, context)

    elif query.data == "setNameForCreateTask":
      return await SetNameTaskHandler.handle(update, context)
    elif query.data == "setDescriptionForCreateTask":
      return await SetDescriptionForCreateTaskHandler.handle(update, context)
    elif query.data == "setDeadlineForCreateTask":
      return await SetDeadlineForCreateTaskHandler.handle(update, context)

    # Обработка кнопок календаря
    elif query.data.startswith("day_"):
      return await TextHandler.handle(update, context)

    elif query.data.startswith("prev_") or query.data.startswith("next_"):
      _, year, month = query.data.split("_")
      year, month = int(year), int(month)
      if context.user_data["state"] == "setDeadlineForTask":
        return await SetDeadlineForCreateTaskHandler.handle(update, context, year, month)
      else:
        return await EditDeadlineHandler.handle(update, context, year, month)

    elif query.data == "setPriorityForCreateTask":
      return await SetPriorityForTaskHandler.handle(update, context)
    elif query.data.startswith("priorityTask"):
       return await TextHandler.handle(update, context)

    elif query.data == "setStatusForCreateTask":
        return await SetStatusForCreateTaskHandler.handle(update, context)
    elif query.data.startswith("statusTask"):
       return await TextHandler.handle(update, context)

    elif query.data == "setDeveloperForCreateTask":
      return await SetDeveloperForTaskHandler.handle(update, context)
    elif query.data.startswith("chosenDeveloperForTask_"):
       return await TextHandler.handle(update, context)

    elif query.data == "saveNewTaskForCreateTask":
        return await SaveCreateTaskHandler.handle(update,context)
    elif query.data == "cancelCreateTask":
        return await CancelCreateTaskHandler.handle(update,context)
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
    elif query.data == "editTaskDeveloper":
      return await EditDeveloperForTaskHandler.handle(update, context)
    elif query.data == "saveEditTask":
      return await SaveEditTaskHandler.handle(update,context)
    elif query.data == "cancelEditTask":
      return await CancelEditTaskHandler.handle(update,context)

    elif query.data.startswith("chosenProject_"):
      context.user_data["chosenProject"] = query.data[14:]
      if context.user_data["state"] == "showProjectsInfo":
        context.user_data["state"] = None
        return await ShowProjectsInfoHandler.handle(update, context)

      elif context.user_data["state"] == "changeProject":
        context.user_data["state"] = None
        return await ChangeProjectHandler.handle(update, context)

      elif context.user_data["state"] == "deleteProject":
        context.user_data["state"] = None
        return await ConfirmationDeleteProjectHandler.handle(update, context)

      elif context.user_data["state"] == "get_project_report":
        context.user_data["state"] = None
        return await ProjectReportHandler.handle(update, context)
      
      elif context.user_data["state"] == "Plan":
        return await GeneratePlanHandler.handle(update, context)

      elif context.user_data["state"] == "chooseDeveloper":
        context.user_data["state"] =  "get_developer_report"
        return await ChooseDeveloperHandler.handle(update, context)

      elif context.user_data["state"] == "currentTasks":
        context.user_data["state"] = None
        return await CurrentTasksHandler.handle(update, context)

    elif query.data.startswith("chosenTask_"):
      context.user_data["chosenTask"] = query.data[11:]
      print(query.data[11:])

      if context.user_data["state"] == "editTask":
        context.user_data["state"] = None
        return await EditTaskMenuHandler.handle(update, context)
      elif context.user_data["state"] == "deleteTask":
        context.user_data["state"] = None
        return await ConfirmationDeleteTaskHandler.handle(update, context)

    elif query.data.startswith("chosenDeveloper_"):
      context.user_data["chosenDeveloper"] = query.data[16:]
      if context.user_data["state"] == "setDeveloperForTask":
        return await TextHandler.handle(update, context)

      elif context.user_data["state"] == "EditTaskDeveloper":
        return await TextHandler.handle(update, context)

      elif context.user_data["state"] == "get_developer_report":
        context.user_data["state"] = None
        return await UserReportHandler.handle(update, context)

    else:
      pass
