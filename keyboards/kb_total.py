from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

# Клавиатура для выбора роли
client: InlineKeyboardButton = InlineKeyboardButton(text='Клиент', callback_data='client')
admin: InlineKeyboardButton = InlineKeyboardButton(text='Эксперт', callback_data='admin')
kb_role: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[client, admin]])


# Функция, которая создает инлайн-кнопки со всеми записями клиента
async def kb_clients_appointments(appoint_times: list):
    kb_clients_appointments_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    b_appointments = []
    appoint_times = sorted(appoint_times, key=lambda x: (x[0], x[1]))
    for appoint in appoint_times:
        b_appointments.append(InlineKeyboardButton(text=(f'{datetime.strftime(datetime.strptime(appoint[0], "%Y-%m-%d"), "%d.%m.%Y")} в {appoint[1]}'), callback_data=(f'app {appoint[1]} {appoint[0]}')))

    b_appointments.append(InlineKeyboardButton(text='Вернуться', callback_data='back_to_begining'))

    kb_clients_appointments_builder.row(*b_appointments, width=1)
    return kb_clients_appointments_builder

# Кнопка с ссылкой на телеграм-аккаунт
telegram: InlineKeyboardButton = InlineKeyboardButton(text='Написать в ТГ ->', url='https://t.me/kabzal')
kb_telega: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[telegram]])