from aiogram import types, Router
from aiogram.filters import Command
from .buttons import BUTTONS
from .messages import START_MESSAGE

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=button["text"], url=button["url"])]
            for button in BUTTONS
        ]
    )

    await message.answer(START_MESSAGE, reply_markup=keyboard)
