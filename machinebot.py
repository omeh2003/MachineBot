import datetime
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_TOKEN, ADMIN_ID
from config import allowed_users

# Создаем простой логер. Советую иметь привыску всегда создавать логеры до того как они вам понадобятся.
date_now = datetime.datetime.now()
log_filename = f'app_{date_now.day}_{date_now.month}_{date_now.year}.log'
if os.path.exists(log_filename):
    os.remove(log_filename)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename,
                    filemode="a", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("Создание логера...")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

input_history = {}


def log_message(message: types.Message):

    try:
        for attr in dir(message):
            if not callable(getattr(message, attr)) and not attr.startswith("__"):
                value = getattr(message, attr)
                if value is not None:
                    if isinstance(value, (str, int, float, bool)):
                        logger.info(f"{attr}: {value}")
                    else:
                        logger.info(f"{attr}: {value.__class__.__name__}")

    except Exception as e:
        logger.error(f"Ошибка при логировании объекта Message: {e}")


def create_input_keyboard():
    keyboard = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['Сброс', '0', 'Отправить']
    ]

    markup = InlineKeyboardMarkup()
    for row in keyboard:
        row_buttons = [InlineKeyboardButton(text=btn_text, callback_data=f"input:{btn_text}") for btn_text in row]
        markup.row(*row_buttons)
    markup.add(InlineKeyboardButton("Отмена", callback_data="cancel"))

    return markup


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    log_message(message)
    if message.from_user.id in ADMIN_ID:
        await show_admin_menu(message)
    if message.from_user.id in allowed_users:
        await message.p(message.chat.id, text="Добро пожаловать пользователь!")
    else:
        await message.reply("Вы не имеете доступа к этому боту.")


async def show_admin_menu(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Добавить пользователя", callback_data="add_user"))
    markup.add(InlineKeyboardButton("Просмотреть пользователей", callback_data="view_users"))

    await message.reply("Выберите действие:", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "add_user")
async def process_add_user(call: types.CallbackQuery):
    markup = create_input_keyboard()
    input_history[call.from_user.id] = ''
    await call.message.reply("Введите ID пользователя, которого хотите добавить:", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith("input:"))
async def process_input(call: types.CallbackQuery):
    input_value = call.data.split(':')[1]

    if input_value == 'Сброс':
        input_history[call.from_user.id] = ''
    elif input_value == 'Отправить':
        if not input_history[call.from_user.id]:
            await call.answer("Введите хотя бы одну цифру перед отправкой.", show_alert=True)
            return

        user_id = int(input_history[call.from_user.id])
        allowed_users.add(user_id)
        await call.message.reply(f"Пользователь с ID {user_id} успешно добавлен.")
        input_history[call.from_user.id] = ''
        await show_admin_menu(call.message)
    else:
        input_history[call.from_user.id] += input_value

    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith("remove_user:"))
async def process_remove_user(call: types.CallbackQuery):
    user_id = int(call.data.split(':')[1])

    if call.from_user.id == user_id:
        await call.answer("Вы не можете удалить себя из списка.")
        return

    allowed_users.discard(user_id)
    await call.answer(f"Пользователь с ID {user_id} успешно удален.")
    await process_view_users(call)


@dp.callback_query_handler(lambda call: call.data == "view_users")
async def process_view_users(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()

    for user_id in allowed_users:
        markup.add(InlineKeyboardButton(str(user_id), callback_data=f"remove_user:{user_id}"))

    markup.add(InlineKeyboardButton("Отмена", callback_data="cancel"))

    await call.message.edit_text("Список пользователей с доступом:", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "cancel")
async def process_cancel(call: types.CallbackQuery):
    await show_admin_menu(call.message)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
