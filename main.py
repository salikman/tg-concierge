import logging
from aiogram import Bot, Dispatcher, executor, types
from db import Database
import markups as nav

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6755457379:AAHYpY0RqI69Xo0xezQ0aBFnqzaUPZK8cno")
dp = Dispatcher(bot)
db = Database('db_users.db')

# Описуємо правила
# rules = """
# Вітаємо на каналі Кулінарні Витівки! 🍳🥗 

# Тут ви знайдете найсмачніші рецепти, цікаві кулінарні поради та захопливі історії про кулінарні подорожі. 

# Натисніть /start, щоб розпочати свою кулінарну подорож разом з нами! 

# Пам'ятайте, натискаючи /start, ви підтверджуєте, що ви не бот, а справжня людина з апетитом до нових смаколиків. 
# """

@dp.message_handler(commands=['start'])
async def start(message: types.Message):  
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "rules", reply_markup=nav.keyboard)

@dp.message_handler(commands=['sendall'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 331075928:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except: 
                    db.set_active(row[0], 0)
                
            await bot.send_message(message.from_user.id, "Done!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)