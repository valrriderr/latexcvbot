from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from main import dp

class CVForm(StatesGroup):
    name = State()
    phone = State()
    email = State()
    github = State()
    linkedin = State()

@dp.message_handler(commands="create")
async def start_create(message: types.Message):
    await message.answer("Как тебя зовут?")
    await CVForm.name.set()

@dp.message_handler(state=CVForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажи номер телефона:")
    await CVForm.next()

@dp.message_handler(state=CVForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введи email:")
    await CVForm.next()

@dp.message_handler(state=CVForm.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введи username GitHub:")
    await CVForm.next()

@dp.message_handler(state=CVForm.github)
async def process_github(message: types.Message, state: FSMContext):
    await state.update_data(github=message.text)
    await message.answer("Введи username LinkedIn:")
    await CVForm.next()

@dp.message_handler(state=CVForm.linkedin)
async def process_linkedin(message: types.Message, state: FSMContext):
    await state.update_data(linkedin=message.text)
    data = await state.get_data()
    summary = "\n".join([f"{key}: {value}" for key, value in data.items()])
    await message.answer(f"Вот что ты ввёл:\n{summary}\nСкоро будет создан PDF…")
    await state.finish()