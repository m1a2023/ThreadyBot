import asyncio
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any


from LLMgen.GeneratePlan import generateProjectPlan
from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForGeneratingProjectPlan.GeneratingProjectPlanMenuHandler import GeneratingPlanMenuHandler
from Handlers.RequestsHandler import getProjectById
from ProjectManagment.ProjectManager import ProjectManager

from LLMgen.GeneratePlan import generateProjectPlan


from LLMgen.GenerateTasks import generateSubProjectPlan, generateProjectTasks


class SaveGeneratedPlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query

        await query.answer()

        await query.edit_message_text(f'(1/2)   Подождите, идет обработка вашего плана...')

        try:

            context.user_data['current_plan'] = context.user_data['temp_plan']
            context.user_data['temp_plan'] = None

            generated_sub_plan = await generateSubProjectPlan(context.user_data['current_plan'])

            # Сообщаем, что идет генерация задач
            await query.edit_message_text(f'(2/2)   Подождите, идет генерация задач...')

            generated_tasks = await generateProjectTasks(generated_sub_plan)

            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="generate_menu")],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)


            json_string = generated_tasks.strip('```').strip()
            try:
                json_data = json.loads(json_string)

                formatted_json = json.dumps(json_data, ensure_ascii=False, indent=4)
                print(formatted_json)


                res = ''
                for i, task in enumerate(json_data):
                    # Тут надо прикрутить заполнение задач в бд
                    name = task.get('name')
                    description = task.get('description')
                    deadline = task.get('deadline')

                    res += f"{i}. Задача: {name}\n"
                    res += f"Описание: {description}\n"
                    res += f"Срок выполнения: {deadline}\n\n"

                # Отправляем результат !!!(Отправить не получится, слишком большое сообщение будет)
                #await query.edit_message_text(f'Ваши задачи: \n{res}')
                print(res)
                await query.edit_message_text(f'Задачи добавлены!', reply_markup=reply_markup)




            except json.JSONDecodeError as e:
                await query.edit_message_text(f'Произошла ошибка декодирования: {str(e)}\nОтвет от нейросети: \n{generated_tasks}',reply_markup=reply_markup)



        except Exception as e:

            await query.edit_message_text(f'Произошла ошибка: {str(e)}',reply_markup=reply_markup)


        #return await GeneratingPlanMenuHandler.handle(update, context)

