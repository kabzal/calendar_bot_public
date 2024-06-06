from aiogram import Router
from aiogram.types import Message

router: Router = Router()

@router.message()
async def any_message_process(message:Message):
    await message.answer(text='Извините, я Вас не понимаю')