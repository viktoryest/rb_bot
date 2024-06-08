import json
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from src.utils import load_markdown

router = Router()


def load_buttons(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


messages_data = {
    "START_MESSAGE": load_markdown('files/START_MESSAGE.md'),
}

BUTTONS = load_buttons('files/buttons.json')


@router.message(Command("start"))
async def start_command(message: types.Message):
    row_width = 2
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button) for button in BUTTONS]],
        resize_keyboard=True,
        row_width=row_width
    )

    await message.answer(messages_data['START_MESSAGE'], reply_markup=keyboard)
