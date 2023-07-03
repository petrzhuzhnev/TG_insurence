import os

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    KeyboardButton('Страхование машины'),
    KeyboardButton('ДМС'),
    KeyboardButton('Страхование жизни'),
    KeyboardButton('Страхование квартиры')
]
keyboard.add(*buttons)

# Создание вложенных кнопок для каждой страховой услуги
car_insurance_keyboard = InlineKeyboardMarkup(row_width=2)
car_insurance_buttons = [
    InlineKeyboardButton('Полная страховка автомобиля', callback_data='full_car_insurance'),
    InlineKeyboardButton('Страховка от угона', callback_data='car_theft_insurance'),
    InlineKeyboardButton('Страховка от ДТП', callback_data='car_accident_insurance')
]
car_insurance_keyboard.add(*car_insurance_buttons)

dms_keyboard = InlineKeyboardMarkup(row_width=1)
dms_buttons = [
    InlineKeyboardButton('Основные медицинские услуги', callback_data='basic_medical_services'),
    InlineKeyboardButton('Расширенный пакет ДМС', callback_data='advanced_dms_package')
]
dms_keyboard.add(*dms_buttons)

life_insurance_keyboard = InlineKeyboardMarkup(row_width=1)
life_insurance_buttons = [
    InlineKeyboardButton('Страхование жизни на случай смерти', callback_data='life_insurance_death'),
    InlineKeyboardButton('Инвестиционное страхование жизни', callback_data='investment_life_insurance')
]
life_insurance_keyboard.add(*life_insurance_buttons)

home_insurance_keyboard = InlineKeyboardMarkup(row_width=2)
home_insurance_buttons = [
    InlineKeyboardButton('Страхование от пожара', callback_data='fire_insurance'),
    InlineKeyboardButton('Страхование имущества', callback_data='property_insurance'),
    InlineKeyboardButton('Страхование от затопления', callback_data='flood_insurance')
]
home_insurance_keyboard.add(*home_insurance_buttons)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Привет! Я бот страхового агента. Как я могу вам помочь?', reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply('Вы можете отправить мне информацию о вашей страховой потребности, и я помогу вам с выбором подходящей страховки.', reply_markup=keyboard)

@dp.message_handler()
async def echo_handler(message: types.Message):
    user_message = message.text
    if user_message == 'Страхование машины':
        await message.reply('Выберите вид страховки для автомобиля:', reply_markup=car_insurance_keyboard)
    elif user_message == 'ДМС':
        await message.reply('Выберите тип пакета ДМС:', reply_markup=dms_keyboard)
    elif user_message == 'Страхование жизни':
        await message.reply('Выберите тип страхования жизни:', reply_markup=life_insurance_keyboard)
    elif user_message == 'Страхование квартиры':
        await message.reply('Выберите вид страхования для квартиры:', reply_markup=home_insurance_keyboard)

@dp.callback_query_handler(lambda c: c.data in ['full_car_insurance', 'car_theft_insurance', 'car_accident_insurance'])
async def car_insurance_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply('Вы выбрали страховку для автомобиля: ' + callback_query.data)

@dp.callback_query_handler(lambda c: c.data in ['basic_medical_services', 'advanced_dms_package'])
async def dms_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply('Вы выбрали тип пакета ДМС: ' + callback_query.data)

@dp.callback_query_handler(lambda c: c.data in ['life_insurance_death', 'investment_life_insurance'])
async def life_insurance_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply('Вы выбрали тип страхования жизни: ' + callback_query.data)

@dp.callback_query_handler(lambda c: c.data in ['fire_insurance', 'property_insurance', 'flood_insurance'])
async def home_insurance_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.reply('Вы выбрали вид страхования для квартиры: ' + callback_query.data)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)