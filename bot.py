import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from dotenv import load_dotenv

from s3_utils import upload_file, generate_download_link
from db import init_db, add_user, add_resume

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

init_db()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.full_name)
    await message.answer("Привет! Отправь PDF-файл, и я загружу его в S3.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_file(message: types.Message):
    document = message.document

    file_path = f"downloads/{document.file_name}"
    await document.download(destination_file=file_path)

    key = f"user_{message.from_user.id}/{document.file_name}"
    s3_url = upload_file(file_path, key)
    add_resume(message.from_user.id, document.file_name)

    link = generate_download_link(key)
    await message.answer(f"Файл загружен. Вот ссылка (действует 10 минут):\n{link}")

if __name__ == '__main__':
    executor.start_polling(dp)
