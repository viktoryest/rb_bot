import json

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton

from .buttons import BUTTONS

with open('./handlers/messages.json', encoding='utf-8') as f:
    messages_data = json.load(f)

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button["text"], url=button["url"]) if button.get("url") else
         InlineKeyboardButton(text=button["text"], callback_data=button["callback_data"])]
        for button in BUTTONS
    ])

    await message.answer(messages_data['START_MESSAGE'], reply_markup=keyboard)
