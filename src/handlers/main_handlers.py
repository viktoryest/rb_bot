import os
import json
import re

from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

with open('./handlers/messages.json', encoding='utf-8') as f:
    messages_data = json.load(f)

router = Router()

load_dotenv()
PRIVATE_CHANNEL_ID = os.getenv('PRIVATE_CHANNEL_ID')


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()


@router.callback_query(lambda c: c.data == 'about_us')
async def handle_about_us(callback_query: types.CallbackQuery):
    media_folder = 'media/about_us'
    media_files = [os.path.join(media_folder, file) for file in os.listdir(media_folder) if
                   file.lower().endswith(('png', 'jpg', 'jpeg'))]

    media_content = []

    for index, media_file in enumerate(media_files):
        fs_input_file = FSInputFile(media_file)
        if index == 0:
            media_content.append(
                types.InputMediaPhoto(media=fs_input_file, caption=messages_data['CAPTION_ABOUT_US'],
                                      parse_mode='HTML'))
        else:
            media_content.append(types.InputMediaPhoto(media=fs_input_file))

    await callback_query.message.answer_media_group(media_content)


@router.callback_query(lambda callback_query: callback_query.data == "requisites")
async def handle_requisites(callback_query: types.CallbackQuery):
    await callback_query.message.answer(messages_data['REQUISITES'], disable_web_page_preview=True)


@router.callback_query(lambda callback_query: callback_query.data == "reports")
async def handle_reports(callback_query: types.CallbackQuery):
    await callback_query.message.answer(messages_data['REPORTS'], disable_web_page_preview=True)


@router.callback_query(lambda callback_query: callback_query.data == "partners")
async def handle_partners(callback_query: types.CallbackQuery):
    await callback_query.message.answer(messages_data['PARTHNERS'], disable_web_page_preview=True)


@router.callback_query(lambda callback_query: callback_query.data == "socials")
async def handle_socials(callback_query: types.CallbackQuery):
    await callback_query.message.answer(messages_data['SOCIAL_MEDIA'], disable_web_page_preview=True)


@router.callback_query(lambda callback_query: callback_query.data == "feedback")
async def handle_feedback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(messages_data['FEEDBACK'], disable_web_page_preview=True)
    await state.set_state(FeedbackForm.waiting_for_feedback)


@router.message(StateFilter(FeedbackForm.waiting_for_feedback))
async def process_feedback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.bot.send_message(int(PRIVATE_CHANNEL_ID), f"Новое сообщение от {message.from_user.full_name} "
                                                            f"(@{message.from_user.username}):\n\n{message.text}"
                                                            f"\n\n/user_{user_id}",
                                   parse_mode='HTML')
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
        await message.bot.send_message(int(user_id), f"Ваше сообщение было прочитано и получило ответ:\n\n"
                                                      f"{message.text}", parse_mode='HTML')
    else:
        await message.answer("Не удалось отправить ответ пользователю.")
