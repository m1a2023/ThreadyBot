from __future__ import annotations



from src.config import IAM_TOKEN, FOLDER_ID

from yandex_cloud_ml_sdk import YCloudML

from ..ProjectManagment.Project import Project


async def GaneratePlan(project : Project):

    result = []

    title = project.get_name()
    description = project.get_description()
    team = len(project.get_team())
    done_tasks = ''


    messages = [
        {
            "role": "system",
            "text": "Ты — опытный проджект менеджер. Напиши план выполнения для следующего проекта по задачам, с учетом названия, описания и количества сотрудников. Каждую задачу разделяй на отдельные подзадачи. Если есть уже сделанные задачи, учти их.",
        },
        {
            "role": "user",
            "text": f"name : {title} "
                    f"description: {description}"
                    f"team: {team}"
                    f"done_tasks: {done_tasks}",
        },
    ]

    sdk = YCloudML(
        folder_id=FOLDER_ID,
        auth=IAM_TOKEN,
    )

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.2).run(messages)
    )

    return result.text