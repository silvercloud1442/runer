from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiohttp import ClientSession
import re

token = '7076655539:AAEyzHEHJLyjOOESREFPprLGbPIMDls6oxA'

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

class PassState(StatesGroup):
    pas = State()

class RegisterState(StatesGroup):
    phone = State()

class ReportState(StatesGroup):
    text = State()


async def get_users():
    path = "http://127.0.0.1:5000/get_user"
    async with ClientSession() as session:
        async with session.get(path) as response:
            data = await response.json()
            return data

async def get_orders(id):
    path = "http://127.0.0.1:5000/get_orders"
    params = {'telegram_id': id}
    async with ClientSession() as session:
        async with session.post(path, params=params) as response:
            data = await response.json()
            return data

@dp.message_handler(state='*', commands=['start'])
async def start(message):
    await bot.send_message(message.from_user.id, "Введите /orders для просмотра заказов")

@dp.callback_query_handler(text_startswith="report")
async def report_grade(call):
    splited = call.data.split('_')
    worker, user, grade = splited[1], splited[2], splited[3]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Text report', callback_data='text_report'))
    await bot.send_message(user, f'{worker}: take grade {grade}', reply_markup=markup)

@dp.callback_query_handler(text='text_report')
async def report_text(call):
    await bot.send_message(call.from_user.id, 'Send report text')
    await ReportState.text.set()

@dp.callback_query_handler(text="create_user")
async def create_user(call):
    await call.message.answer('Vedite nomer v formate +71112223344')
    await RegisterState.phone.set()

@dp.message_handler(state='*', commands=['orders'])
async def is_registred(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Create", callback_data="create_user"))
    users = await get_users()
    phone = False
    for user in users:
        if user['telegram_id'] == message.from_user.id:
            phone = user['phone']
            break
    if phone:
        orders = await get_orders(message.from_user.id)
        await bot.send_message(message.from_user.id, orders)
    else:
        await bot.send_message(message.from_user.id, "user not found. Create?", reply_markup=markup)

@dp.message_handler(state=RegisterState.phone)
async def set_phone(message):
    phone = message.text
    if re.match("^((\+7)+([0-9]){10})$", phone):
        await bot.send_message(message.from_user.id, "correct")
        await PassState.pas.set()
    else:
        await bot.send_message(message.from_user.id, "NOT correct")



@dp.message_handler(state=ReportState.text)
async def report_text(message):
    await bot.send_message(message.from_user.id, f'SEND REPORT WITH: {message.text}')
    await PassState.pas.set()

executor.start_polling(dp)