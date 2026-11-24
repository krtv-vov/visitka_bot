import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    Update,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    FSInputFile,
)
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "9037503874:AAGKKDmWb4jO3hj4bDFJKI4s6ZOeXIzr5N4"
MY_USERNAME = "aeeeqk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


def get_image(filename: str) -> FSInputFile:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "img", filename)
    return FSInputFile(img_path)


def get_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💻 Разработка (Боты / Сайты)", callback_data="show_dev")
    kb.button(text="🛠 Помощь с ПК (Удаленно)", callback_data="show_pc")
    kb.button(text="🎨 Графический дизайн", callback_data="show_design")
    kb.button(text="👤 Мои работы и Отзывы", url="https://t.me/+4HX3Qi92GnAyNTM6")
    kb.button(text="💬 Написать мне лично", url=f"https://t.me/{MY_USERNAME}")
    return kb.adjust(1, 1, 1, 2).as_markup()


def get_service_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Обсудить задачу", url=f"https://t.me/{MY_USERNAME}")
    kb.button(text="🔙 Назад в меню", callback_data="back_to_main")
    return kb.adjust(1).as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "Привет! Я Павел — частный IT-специалист и разработчик.\n\n"
        "Выполняю задачи быстро, работаю на результат. Выберите интересующее направление ниже, "
        "чтобы узнать подробности и цены, или сразу пишите мне в личные сообщения."
    )
    await message.answer(text, reply_markup=get_main_menu())


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(call: CallbackQuery):
    text = "Выберите интересующее направление:"
    try:
        await call.message.edit_text(text, reply_markup=get_main_menu())
    except Exception:
        await call.message.delete()
        await call.message.answer(text, reply_markup=get_main_menu())


@dp.callback_query(F.data == "show_dev")
async def show_dev(call: CallbackQuery):
    text = (
        "<b>💻 Программирование и Разработка</b>\n\n"
        "• <b>Telegram-боты</b> (aiogram, API, базы данных) — <b>от 2 500 рублей</b>\n"
        "• <b>Лендинги и сайты-визитки</b> под ключ — <b>от 4 000 рублей</b>\n"
        "• <b>Скрипты автоматизации и парсинг</b> (Python) — <b>от 1 500 рублей</b>\n\n"
        "Итоговая сумма зависит от сложности логики, интеграций и объема задач.\n\n"
        "<i>Точную стоимость назову после короткого обсуждения вашей задачи. Это бесплатно. "
        "Нажмите кнопку ниже, чтобы обсудить проект.</i>"
    )
    media = InputMediaPhoto(media=get_image("dev.jpg"), caption=text, parse_mode="HTML")
    await call.message.edit_media(media=media, reply_markup=get_service_menu())


@dp.callback_query(F.data == "show_pc")
async def show_pc(call: CallbackQuery):
    text = (
        "<b>🛠 Удаленная помощь с ПК</b>\n\n"
        "• <b>Удаленная настройка и решение проблем</b> (AnyDesk / RuDesk) — <b>от 700 рублей</b>\n"
        "• <b>Установка и оптимизация Windows, драйверов и ПО</b> — <b>от 1 000 рублей</b>\n"
        "• <b>Чистка системы от вирусов и ускорение работы</b> — <b>от 800 рублей</b>\n\n"
        "Базовое подключение и решение типовых задач входят в стоимость старта; если работа затягивается "
        "или требует глубокой настройки — применяется почасовая ставка <b>от 500 рублей/час</b>.\n\n"
        "<i>Точную стоимость назову после короткого обсуждения вашей задачи. Это бесплатно. "
        "Жмите кнопку для связи.</i>"
    )
    media = InputMediaPhoto(media=get_image("pc.jpg"), caption=text, parse_mode="HTML")
    await call.message.edit_media(media=media, reply_markup=get_service_menu())


@dp.callback_query(F.data == "show_design")
async def show_design(call: CallbackQuery):
    text = (
        "<b>🎨 Графический дизайн</b>\n\n"
        "• <b>Логотипы и фирменный стиль</b> — <b>от 1 500 рублей</b>\n"
        "• <b>Рекламные баннеры и оформление соцсетей</b> — <b>от 600 рублей</b>\n"
        "• <b>Карточки для маркетплейсов и визитки</b> — <b>от 500 рублей</b> (за карточку/макет)\n\n"
        "Вся работа ведется в <b>Photoshop</b> — аккуратно, с учетом задач и формата площадки.\n\n"
        "<i>Точную стоимость назову после короткого обсуждения вашей задачи. Это бесплатно. "
        "Напишите мне, чтобы обсудить визуал.</i>"
    )
    media = InputMediaPhoto(media=get_image("design.jpg"), caption=text, parse_mode="HTML")
    await call.message.edit_media(media=media, reply_markup=get_service_menu())


# --- ТОЧКА ВХОДА ДЛЯ VERCEL ---
@app.post("/webhook")
async def webhook_handler(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
