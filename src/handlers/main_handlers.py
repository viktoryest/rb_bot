import os
import json
import re
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from src.utils import load_markdown

router = Router()


def load_links(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


messages_data = {
    "START_MESSAGE": load_markdown('files/START_MESSAGE.md'),
    "CAPTION_ABOUT_US": load_markdown('files/CAPTION_ABOUT_US.md'),
    "REQUISITES": load_markdown('files/REQUISITES.md'),
    "REPORTS": load_markdown('files/REPORTS.md'),
    "PARTHNERS": load_markdown('files/PARTHNERS.md'),
    "SOCIAL_MEDIA": load_markdown('files/SOCIAL_MEDIA.md'),
    "FEEDBACK": load_markdown('files/FEEDBACK.md'),
    "GUIDE": load_markdown('files/GUIDE.md'),
}

links_data = load_links('files/links.json')

load_dotenv()
PRIVATE_CHANNEL_ID = os.getenv('PRIVATE_CHANNEL_ID')


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()


@router.message(F.text == "О нас")
async def handle_about_us(message: types.Message):
    media_folder = 'media/about_us'
    media_files = [os.path.join(media_folder, file) for file in os.listdir(media_folder) if
                   file.lower().endswith(('png', 'jpg', 'jpeg'))]
    media_content = []
    for index, media_file in enumerate(media_files):
        fs_input_file = FSInputFile(media_file)
        if index == 0:
            media_content.append(types.InputMediaPhoto(media=fs_input_file, caption=messages_data['CAPTION_ABOUT_US'],
                                                       parse_mode='HTML'))
        else:
            media_content.append(types.InputMediaPhoto(media=fs_input_file))
    await message.answer_media_group(media_content)


@router.message(F.text == "Реквизиты")
async def handle_requisites(message: types.Message):
    await message.answer(messages_data['REQUISITES'], disable_web_page_preview=True)


@router.message(F.text == "Отчеты о сборах")
async def handle_reports(message: types.Message):
    await message.answer(messages_data['REPORTS'], disable_web_page_preview=True)


@router.message(F.text == "Гайд по Батуми")
async def handle_guide(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section["text"], url=section["url"]) for section in links_data["sections"][i:i + 2]]
        for i in range(0, len(links_data["sections"]), 2)
    ])
    await message.answer("Выберите раздел:", reply_markup=keyboard)


@router.message(F.text == "Наши партнеры")
async def handle_partners(message: types.Message):
    await message.answer(messages_data['PARTHNERS'], disable_web_page_preview=True)


@router.message(F.text == "Наши соцсети")
async def handle_socials(message: types.Message):
    await message.answer(messages_data['SOCIAL_MEDIA'], disable_web_page_preview=True)


@router.message(F.text == "Обратная связь")
async def handle_feedback(message: types.Message, state: FSMContext):
    await message.answer(messages_data['FEEDBACK'], disable_web_page_preview=True)
    await state.set_state(FeedbackForm.waiting_for_feedback)


@router.message(StateFilter(FeedbackForm.waiting_for_feedback))
async def process_feedback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.bot.send_message(
        int(PRIVATE_CHANNEL_ID),
        f"Новое сообщение от {message.from_user.full_name} (@{message.from_user.username}):"
        f"\n\n{message.text}\n\n/user_{user_id}",
        parse_mode='HTML'
    )
    await message.answer("Ваше сообщение отправлено!")
    await state.clear()


@router.channel_post()
async def reply_to_feedback(message: types.Message):
    if not message.reply_to_message:
        return

    original_message = message.reply_to_message
    user_id = re.search(r'/user_(\d+)', original_message.text)
    if user_id:
        user_id = user_id.group(1)
        await message.bot.send_message(
            int(user_id),
            f"Ваше сообщение было прочитано и получило ответ:\n\n{message.text}",
            parse_mode='HTML'
        )
    else:
        await message.answer("Не удалось отправить ответ пользователю.")
