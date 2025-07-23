from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import os
import subprocess
from pdf2image import convert_from_path
from dotenv import load_dotenv

from s3_utils import upload_file, generate_download_link
from db import init_db, add_user, add_resume

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

init_db()

# --- STATES ---
class ResumeStates(StatesGroup):
    skills_group = State()
    skills_next = State()
    experience = State()
    experience_next = State()
    education_name = State()
    education_level = State()
    education_specialty = State()
    education_start = State()
    education_end = State()
    education_next = State()
    final_review = State()

# --- LaTeX/PDF/PNG FUNCTIONS ---
def render_latex_to_pdf(latex_code: str, output_dir: str, filename: str = "resume"):
    tex_path = os.path.join(output_dir, f"{filename}.tex")
    pdf_path = os.path.join(output_dir, f"{filename}.pdf")
    with open(tex_path, "w") as f:
        f.write(latex_code)
    subprocess.run(["pdflatex", "-output-directory", output_dir, tex_path], check=True)
    return pdf_path

def pdf_to_png(pdf_path: str, output_dir: str, filename: str = "resume"):
    images = convert_from_path(pdf_path, dpi=200)
    image_path = os.path.join(output_dir, f"{filename}.png")
    images[0].save(image_path, "PNG")
    return image_path

# --- KEYBOARDS ---
def yes_no_kb():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Да", "Нет")
    return keyboard

# --- START ---
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    add_user(message.from_user.id, message.from_user.full_name)
    await message.answer("Привет! Я помогу создать LaTeX-резюме. Добавим навыки?", reply_markup=yes_no_kb())
    await ResumeStates.skills_group.set()

@dp.message_handler(commands=["create"])
async def create_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Давай начнём создание нового резюме! Добавим навыки?", reply_markup=yes_no_kb())
    await ResumeStates.skills_group.set()

# --- Остальные хендлеры остаются без изменений ---
# ...

# --- FINAL REVIEW ---
async def go_to_review(message, state):
    data = await state.get_data()
    latex_code = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}
\section*{Навыки}
%s

\section*{Опыт работы}
%s

\section*{Образование}
%s
\end{document}
""" % (
        "\n".join([f"\\textbf{{{g['group']}}}: {', '.join(g['items'])}" for g in data.get('skills', [])]),
        "\n\n".join([f"{e['company']} -- {e['position']} ({e['period']}):\\\\" + ", ".join(e['duties']) for e in data.get('experience', [])]),
        "\n".join([f"{e['name']} ({e['level']}, {e['specialty']}, {e['start']}-{e['end']})" for e in data.get('education', [])])
    )

    output_dir = "./user_resumes"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"resume_{message.from_user.id}"

    try:
        pdf_path = render_latex_to_pdf(latex_code, output_dir, filename)
        png_path = pdf_to_png(pdf_path, output_dir, filename)

        # Загрузка на S3
        s3_key_pdf = f"user_{message.from_user.id}/{filename}.pdf"
        upload_file(pdf_path, s3_key_pdf)
        add_resume(message.from_user.id, s3_key_pdf)
        link = generate_download_link(s3_key_pdf)

        await message.answer("Спасибо! Твоё резюме готово. Вот ссылка на PDF (действует 10 минут):")
        await message.answer(link)

        with open(png_path, 'rb') as img_file:
            await message.answer_photo(img_file, caption="Ваше резюме (PNG)")

    except Exception as e:
        await message.answer(f"Произошла ошибка при сборке резюме: {e}")

    await state.finish()

# --- RUN BOT ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)