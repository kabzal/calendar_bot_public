from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.general_lex import MAIN_MENU


# Функция для формирования главного меню команд
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in MAIN_MENU.items()]
    await bot.set_my_commands(main_menu_commands)