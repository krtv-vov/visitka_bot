import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, Update, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения Vercel")

MY_USERNAME = "aeeeqk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


def get_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💻 Разработка", callback_data="show_dev")
    kb.button(text="🛠 Помощь с ПК", callback_data="show_pc")
    kb.button(text="🎨 Графический дизайн", callback_data="show_design")
    kb.button(text="⭐ Кейсы и отзывы", url="https://t.me/+4HX3Qi92GnAyNTM6")
    kb.button(text="💬 Личка", url=f"https://t.me/{MY_USERNAME}")
    return kb.adjust(1, 1, 1, 2).as_markup()


def get_service_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Обсудить задачу", url=f"https://t.me/{MY_USERNAME}")
    kb.button(text="🔙 Назад в меню", callback_data="back_to_main")
    return kb.adjust(1).as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "Привет! Я частный специалист: занимаюсь разработкой ботов и сайтов, "
        "удалённой помощью с ПК и графическим дизайном.\n\n"
        "Выбери раздел ниже, чтобы посмотреть услуги и цены, или сразу напиши в личку."
    )
    await message.answer(text, reply_markup=get_main_menu())


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(call: CallbackQuery):
    text = "Выбери раздел ниже, чтобы посмотреть услуги и цены, или сразу напиши в личку."
    await call.message.edit_text(text, reply_markup=get_main_menu())


@dp.callback_query(F.data == "show_dev")
async def show_dev(call: CallbackQuery):
    text = (
        "<b>💻 Разработка</b>\n\n"
        "• Telegram-боты (aiogram, API, базы данных) — <b>от 2 500 ₽</b>\n"
        "• Лендинги и сайты-визитки под ключ — <b>от 4 000 ₽</b>\n"
        "• Скрипты автоматизации и парсинг (Python) — <b>от 1 500 ₽</b>\n\n"
        "Итог зависит от логики, интеграций и объёма. Точную цену скажу после короткого "
        "обсуждения задачи — это бесплатно. Жми кнопку ниже, чтобы обсудить проект."
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())


@dp.callback_query(F.data == "show_pc")
async def show_pc(call: CallbackQuery):
    text = (
        "<b>🛠 Помощь с ПК</b>\n\n"
        "• Консультация по задаче — <b>бесплатно</b>\n"
        "• Удалённая настройка и решение проблем (AnyDesk / RuDesk) — <b>от 700 ₽</b>\n"
        "• Выездная помощь с ПК — <b>500 ₽</b>\n"
        "• Установка и настройка Windows, драйверов и ПО — <b>от 1 000 ₽</b>\n"
        "• Чистка от вирусов и ускорение системы — <b>от 800 ₽</b>\n\n"
        "Типовые задачи входят в старт; если работа затягивается или требует глубокой настройки — "
        "<b>от 500 ₽/час</b>. Точную стоимость назову бесплатно после короткого обсуждения задачи — "
        "жми кнопку ниже."
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())


@dp.callback_query(F.data == "show_design")
async def show_design(call: CallbackQuery):
    text = (
        "<b>🎨 Графический дизайн</b>\n\n"
        "• Логотипы и фирменный стиль — <b>от 1 500 ₽</b>\n"
        "• Рекламные баннеры и оформление соцсетей — <b>от 600 ₽</b>\n"
        "• Карточки для маркетплейсов и визитки — <b>от 500 ₽</b> (за макет)\n\n"
        "Итог зависит от сложности и объёма. Точную стоимость назову бесплатно после короткого "
        "обсуждения задачи — жми кнопку ниже."
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=get_service_menu())


@app.post("/webhook")
async def webhook_handler(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
