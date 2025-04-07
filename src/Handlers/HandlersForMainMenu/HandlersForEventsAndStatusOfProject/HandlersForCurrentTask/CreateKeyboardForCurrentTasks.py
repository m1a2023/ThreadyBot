from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class CreateKeyboardForCurrentTasks:
    @staticmethod
    async def create_tasks_keyboard(todo_tasks, in_progress_tasks):
        keyboard = []
        
        keyboard.append([InlineKeyboardButton("Задачи", callback_data="none")])
        
        # Добавляем заголовки столбцов
        keyboard.append([
            InlineKeyboardButton("🔄 В процессе", callback_data="none"),
            InlineKeyboardButton("◽️ TODO", callback_data="none")
        ])
        
        # Определяем максимальное количество строк
        max_rows = max(len(in_progress_tasks), len(todo_tasks))
        
        # Заполняем строки задачами
        for i in range(max_rows):
            row = []
            
            # Кнопка для задачи "В процессе" (если есть)
            if i < len(in_progress_tasks):
                task = in_progress_tasks[i]
                row.append(InlineKeyboardButton(
                    task['title'], 
                    callback_data=f"taskInCurrentTasks_{task['id']}"
                ))
            else:
                row.append(InlineKeyboardButton(" ", callback_data="none"))
            
            # Кнопка для задачи "TODO" (если есть)
            if i < len(todo_tasks):
                task = todo_tasks[i]
                row.append(InlineKeyboardButton(
                    task['title'], 
                    callback_data=f"taskInCurrentTasks_{task['id']}"
                ))
            else:
                row.append(InlineKeyboardButton(" ", callback_data="none"))
            
            keyboard.append(row)
        
        return keyboard