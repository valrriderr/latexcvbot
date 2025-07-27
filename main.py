from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging, os, subprocess
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
    full_name = State()
    position = State()
    email = State()
    phone = State()
    city = State()
    links = State()
    about = State()
    skills = State()
    experience_start = State()
    experience_company = State()
    experience_role = State()
    experience_period = State()
    experience_desc = State()
    experience_confirm = State()
    education_start = State()
    education_name = State()
    education_degree = State()
    education_specialty = State()
    education_years = State()
    education_confirm = State()
    languages = State()
    certificates = State()
    review = State()
    edit_section = State()
    choose_format = State()

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

# --- FSM LOGIC ---
@dp.message_handler(commands=["start", "create"])
async def cmd_start(message: types.Message, state: FSMContext):
    add_user(message.from_user.id, message.from_user.full_name)
    await state.finish()
    await message.answer("Добро пожаловать! Давайте создадим ваше резюме.\nКак вас зовут?")
    await ResumeStates.full_name.set()

@dp.message_handler(state=ResumeStates.full_name)
async def ask_position(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("Какую должность/роль вы ищете?")
    await ResumeStates.position.set()

@dp.message_handler(state=ResumeStates.position)
async def ask_email(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text.strip())
    await message.answer("Укажите ваш email:")
    await ResumeStates.email.set()

@dp.message_handler(state=ResumeStates.email)
async def ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await message.answer("Ваш номер телефона:")
    await ResumeStates.phone.set()

@dp.message_handler(state=ResumeStates.phone)
async def ask_city(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer("В каком городе вы живёте?")
    await ResumeStates.city.set()

@dp.message_handler(state=ResumeStates.city)
async def ask_links(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text.strip())
    await message.answer("Ссылки на ваши профили (LinkedIn, GitHub) — через запятую или напишите 'нет':")
    await ResumeStates.links.set()

@dp.message_handler(state=ResumeStates.links)
async def ask_about(message: types.Message, state: FSMContext):
    await state.update_data(links=message.text.strip())
    await message.answer("Напишите пару предложений о себе:")
    await ResumeStates.about.set()

@dp.message_handler(state=ResumeStates.about)
async def ask_skills(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text.strip())
    await message.answer("Перечислите ваши ключевые навыки через запятую:")
    await ResumeStates.skills.set()

@dp.message_handler(state=ResumeStates.skills)
async def ask_experience(message: types.Message, state: FSMContext):
    await state.update_data(skills=[x.strip() for x in message.text.split(",")])
    await message.answer("Добавим опыт работы?", reply_markup=yes_no_kb())
    await ResumeStates.experience_start.set()

@dp.message_handler(state=ResumeStates.experience_start)
async def experience_start(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Название компании:", reply_markup=types.ReplyKeyboardRemove())
        await ResumeStates.experience_company.set()
    else:
        await state.update_data(experience=[])
        await ask_education(message, state)

@dp.message_handler(state=ResumeStates.experience_company)
async def experience_role(message: types.Message, state: FSMContext):
    await state.update_data(curr_exp_company=message.text.strip())
    await message.answer("Ваша должность там?")
    await ResumeStates.experience_role.set()

@dp.message_handler(state=ResumeStates.experience_role)
async def experience_period(message: types.Message, state: FSMContext):
    await state.update_data(curr_exp_role=message.text.strip())
    await message.answer("Период работы (например, июнь 2022 — июль 2025):")
    await ResumeStates.experience_period.set()

@dp.message_handler(state=ResumeStates.experience_period)
async def experience_desc(message: types.Message, state: FSMContext):
    await state.update_data(curr_exp_period=message.text.strip())
    await message.answer("Кратко опишите ваши обязанности:")
    await ResumeStates.experience_desc.set()

@dp.message_handler(state=ResumeStates.experience_desc)
async def experience_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    exp = {
        "company": data.get("curr_exp_company"),
        "role": data.get("curr_exp_role"),
        "period": data.get("curr_exp_period"),
        "desc": message.text.strip()
    }
    experience = data.get("experience", [])
    experience.append(exp)
    await state.update_data(experience=experience)
    # Очищаем временные поля
    for k in ["curr_exp_company", "curr_exp_role", "curr_exp_period"]:
        await state.update_data(**{k: None})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Добавить ещё", "Перейти к образованию")
    await message.answer("Добавить ещё одно место работы или перейти к разделу 'Образование'?", reply_markup=keyboard)
    await ResumeStates.experience_confirm.set()

@dp.message_handler(state=ResumeStates.experience_confirm)
async def experience_next_or_education(message: types.Message, state: FSMContext):
    if "ещё" in message.text.lower():
        await message.answer("Название компании:", reply_markup=types.ReplyKeyboardRemove())
        await ResumeStates.experience_company.set()
    else:
        await ask_education(message, state)

async def ask_education(message, state):
    await message.answer("Добавим образование?", reply_markup=yes_no_kb())
    await ResumeStates.education_start.set()

@dp.message_handler(state=ResumeStates.education_start)
async def education_start(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Название учебного заведения:", reply_markup=types.ReplyKeyboardRemove())
        await ResumeStates.education_name.set()
    else:
        await state.update_data(education=[])
        await ask_languages(message, state)

@dp.message_handler(state=ResumeStates.education_name)
async def education_degree(message: types.Message, state: FSMContext):
    await state.update_data(curr_edu_name=message.text.strip())
    await message.answer("Степень (бакалавр, магистр и т.п.):")
    await ResumeStates.education_degree.set()

@dp.message_handler(state=ResumeStates.education_degree)
async def education_specialty(message: types.Message, state: FSMContext):
    await state.update_data(curr_edu_degree=message.text.strip())
    await message.answer("Специальность:")
    await ResumeStates.education_specialty.set()

@dp.message_handler(state=ResumeStates.education_specialty)
async def education_years(message: types.Message, state: FSMContext):
    await state.update_data(curr_edu_specialty=message.text.strip())
    await message.answer("Годы обучения (например, 2020-2024):")
    await ResumeStates.education_years.set()

@dp.message_handler(state=ResumeStates.education_years)
async def education_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    edu = {
        "name": data.get("curr_edu_name"),
        "degree": data.get("curr_edu_degree"),
        "specialty": data.get("curr_edu_specialty"),
        "years": message.text.strip()
    }
    education = data.get("education", [])
    education.append(edu)
    await state.update_data(education=education)
    # Очищаем временные поля
    for k in ["curr_edu_name", "curr_edu_degree", "curr_edu_specialty"]:
        await state.update_data(**{k: None})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Добавить ещё", "Перейти к языкам")
    await message.answer("Добавить ещё одно образование или перейти к языкам?", reply_markup=keyboard)
    await ResumeStates.education_confirm.set()

@dp.message_handler(state=ResumeStates.education_confirm)
async def education_next_or_languages(message: types.Message, state: FSMContext):
    if "ещё" in message.text.lower():
        await message.answer("Название учебного заведения:", reply_markup=types.ReplyKeyboardRemove())
        await ResumeStates.education_name.set()
    else:
        await ask_languages(message, state)

async def ask_languages(message, state):
    await message.answer("Какими языками вы владеете? (например, Английский — свободно, Русский — родной)")
    await ResumeStates.languages.set()

@dp.message_handler(state=ResumeStates.languages)
async def ask_certificates(message: types.Message, state: FSMContext):
    await state.update_data(languages=message.text.strip())
    await message.answer("Хотите добавить информацию о курсах, сертификатах, хобби?", reply_markup=yes_no_kb())
    await ResumeStates.certificates.set()

@dp.message_handler(state=ResumeStates.certificates)
async def show_review(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer("Перечислите курсы, сертификаты или хобби (через запятую):", reply_markup=types.ReplyKeyboardRemove())
        await ResumeStates.review.set()
    else:
        await state.update_data(certificates="")
        await preview_resume(message, state)

@dp.message_handler(state=ResumeStates.review)
async def handle_certificates(message: types.Message, state: FSMContext):
    await state.update_data(certificates=message.text.strip())
    await preview_resume(message, state)

async def preview_resume(message, state):
    data = await state.get_data()
    preview = f"Ваше резюме:\n" \
              f"ФИО: {data.get('full_name')}\n" \
              f"Должность: {data.get('position')}\n" \
              f"Email: {data.get('email')}\n" \
              f"Телефон: {data.get('phone')}\n" \
              f"Город: {data.get('city')}\n" \
              f"Ссылки: {data.get('links')}\n" \
              f"О себе: {data.get('about')}\n" \
              f"Навыки: {', '.join(data.get('skills', []))}\n" \
              f"\nОпыт:\n" + \
              "\n".join([f"{e['company']} / {e['role']} / {e['period']} / {e['desc']}" for e in data.get('experience', [])]) + \
              f"\n\nОбразование:\n" + \
              "\n".join([f"{e['name']} / {e['degree']} / {e['specialty']} / {e['years']}" for e in data.get('education', [])]) + \
              f"\n\nЯзыки: {data.get('languages')}\n" \
              f"\nКурсы/сертификаты: {data.get('certificates')}"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Всё верно", "Исправить")
    await message.answer(preview, reply_markup=keyboard)
    await ResumeStates.edit_section.set()

@dp.message_handler(state=ResumeStates.edit_section)
async def choose_format(message: types.Message, state: FSMContext):
    if message.text.lower() == "всё верно":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("PDF", "Изображение")
        await message.answer("В каком формате хотите получить резюме?", reply_markup=keyboard)
        await ResumeStates.choose_format.set()
    else:
        await message.answer("Напишите, какой раздел вы хотите исправить (например: ФИО, Навыки, Опыт, Образование, Языки, Сертификаты):", reply_markup=types.ReplyKeyboardRemove())
        # Здесь можно реализовать выбор секции для редактирования

@dp.message_handler(state=ResumeStates.choose_format)
async def send_resume_file(message: types.Message, state: FSMContext):
    format_type = message.text.lower()
    data = await state.get_data()

    # --- Формируем LaTeX на основе данных ---
    # Здесь желательно подгрузить classic-blue.tex как шаблон и подставить значения,
    # ниже — пример минимальной вставки в шаблон. Для production лучше использовать jinja2.
    latex_code = r"""
\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}
\geometry{left=1.25cm,right=1.25cm,top=1.25cm,bottom=1.25cm,columnsep=1.2cm}
\usepackage{paracol}
\usepackage{fontawesome5}
\usepackage{hyperref}
\setmainfont{Roboto}
\renewcommand{\familydefault}{\sfdefault}

\name{%s}
\tagline{%s}
\personalinfo{
  \email{%s}
  \phone{%s}
  \location{%s}
  \linkedin{%s}
}

\begin{document}
\makecvheader

\cvsection{О себе}
%s

\cvsection{Навыки}
\cvtag{%s}

\cvsection{Опыт}
%s

\cvsection{Образование}
%s

\cvsection{Языки}
%s

\cvsection{Курсы и сертификаты}
%s

\end{document}
""" % (
        data.get('full_name', ''),
        data.get('position', ''),
        data.get('email', ''),
        data.get('phone', ''),
        data.get('city', ''),
        data.get('links', ''),
        data.get('about', ''),
        "}{".join(data.get('skills', [])),
        "\n".join([f"\\cvevent{{{e['role']}}}{{{e['company']}}}{{{e['period']}}}{{{e['desc']}}}" for e in data.get('experience', [])]),
        "\n".join([f"\\cvevent{{{e['degree']}}}{{{e['name']}}}{{{e['years']}}}{{{e['specialty']}}}" for e in data.get('education', [])]),
        data.get('languages', ''),
        data.get('certificates', '')
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

        if format_type == "pdf":
            await message.answer("Ваше резюме готово! Вот ссылка на PDF (действует 10 минут):")
            await message.answer(link)
        else:
            with open(png_path, 'rb') as img_file:
                await message.answer_photo(img_file, caption="Ваше резюме (PNG)")
    except Exception as e:
        await message.answer(f"Произошла ошибка при сборке резюме: {e}")

    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)