from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Стартовая клавиатура клиента
wish_appoint: InlineKeyboardButton = InlineKeyboardButton(text='Записаться',
                                                          callback_data='show_calendar')
my_appoints: InlineKeyboardButton = InlineKeyboardButton(text='Мои записи',
                                                         callback_data='my_appointments')
new_role: InlineKeyboardButton = InlineKeyboardButton(text='Изменить роль',
                                                      callback_data='change_my_role')

kb_main_client: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[wish_appoint], [my_appoints], [new_role]])


# Функция, которая формирует 2 клавиатуры
# Клавиатура 1: отмена записи и возврат
# Клавиатура 2: подтверждение отмены и возврат
async def kb_ok_cancel_func(current_date, current_time):
    okay: InlineKeyboardButton = InlineKeyboardButton(text='Вернуться',
                                                      callback_data='my_appointments')
    cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись',
                                                        callback_data=('cancel_app' + ' ' + str(current_date) + ' ' + str(current_time)))
    sure_cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись',
                                                             callback_data=('sure_cancel_app' + ' ' + str(current_date) + ' ' + str(current_time)))

    kb_ok_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okay, cancel]])
    kb_sure_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okay, sure_cancel]])
    return [kb_ok_cancel, kb_sure_cancel]


# Функция, которая создает инлайн-кнопки с доступными окнами для записи в заданный день
async def kb_free_times(free_times: list, current_date):
    kb_free_times_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    b_times = []
    free_times = sorted(free_times)
    for time in free_times:
        b_times.append(InlineKeyboardButton(text=str(time), callback_data=('startFSM ' + str(time)+' '+str(current_date))))
    b_times.append(InlineKeyboardButton(text='Вернуться', callback_data='show_calendar'))

    kb_free_times_builder.row(*b_times, width=1)
    return kb_free_times_builder


# Кнопка возврата в календарь
return_to_calendar: InlineKeyboardButton = InlineKeyboardButton(text='Назад в календарь', callback_data='show_calendar')
kb_return_to_calendar: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_calendar]])

# Кнопка возврата в Мои записи
return_to_apps: InlineKeyboardButton = InlineKeyboardButton(text='Назад в мои записи', callback_data='my_appointments')
kb_return_to_apps: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_apps]])