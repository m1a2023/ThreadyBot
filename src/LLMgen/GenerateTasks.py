from __future__ import annotations
from config import IAM_TOKEN, FOLDER_ID
from yandex_cloud_ml_sdk import YCloudML
from ProjectManagment.Project import Project


async def generateSubProjectPlan(plan):
    messages = [
        {
            "role": "system",
            "text": "У тебя есть план выполнения проекта. Перепиши все задачи единым списком (Убери заголовки, оставь только список из подзадач). Было: {Задача1 : Список из подзадач, Задача2 : список из подзадач}  Стало: {Подзадача1 : Описание, Подзадача2 : Описание}",
        },
        {
            "role": "user",
            "text": f"plan : {plan}"
        },
    ]

    sdk = YCloudML(
        folder_id=FOLDER_ID,
        auth=IAM_TOKEN,
    )

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.2).run(messages)
    )

    sub_plan = result.text

    return sub_plan

async def generateProjectTasks(plan):

    sub_plan = await generateSubProjectPlan(plan)

    messages = [
        {
            "role": "system",
            "text": "Ты — опытный проджект менеджер. У тебя есть список задач. Добавь каждой задачи название и срок выполнения. Ответ в виде json файла {name: str, description: str, deadline : str}",
        },
        {
            "role": "user",
            "text": f"plan : {sub_plan}"
        },
    ]

    sdk = YCloudML(
        folder_id=FOLDER_ID,
        auth=IAM_TOKEN,
    )

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.2).run(messages)
    )

