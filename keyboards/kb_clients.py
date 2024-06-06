from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

wish_appoint: InlineKeyboardButton = InlineKeyboardButton(text='Записаться', callback_data='show_calendar')
my_appoints: InlineKeyboardButton = InlineKeyboardButton(text='Мои записи', callback_data='my_appointments')
new_role: InlineKeyboardButton = InlineKeyboardButton(text='Изменить роль', callback_data='change_my_role')
kb_main_client: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[wish_appoint], [my_appoints], [new_role]])

#Функция, которая передает информацию о дате и времени в хендлер для отмены записи клиентом
async def kb_ok_cancel_func(current_date, current_time):
    okey: InlineKeyboardButton = InlineKeyboardButton(text='Вернуться', callback_data='my_appointments')
    cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись', callback_data=('cancel_app' + ' ' + str(current_date) + ' ' + str(current_time)))
    sure_cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись', callback_data=('sure_cancel_app'+ ' ' + str(current_date) + ' ' + str(current_time)))
    kb_ok_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okey, cancel]])
    kb_sure_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okey, sure_cancel]])
    return [kb_ok_cancel, kb_sure_cancel]


#Функция, которая создает инлайн-кнопки с доступным временем для записи в заданный день
async def kb_free_times(free_times: list, current_date):
    kb_free_times_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    b_times = []
    free_times = sorted(free_times)
    for time in free_times:
        b_times.append(InlineKeyboardButton(text=str(time), callback_data=('startFSM ' + str(time)+' '+str(current_date))))
    b_times.append(InlineKeyboardButton(text='Вернуться', callback_data='show_calendar'))
    kb_free_times_builder.row(*b_times, width=1)
    return kb_free_times_builder

return_to_calendar: InlineKeyboardButton = InlineKeyboardButton(text='Назад в календарь', callback_data='show_calendar')
kb_return_to_calendar: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_calendar]])

return_to_apps: InlineKeyboardButton = InlineKeyboardButton(text='Назад в мои записи', callback_data='my_appointments')
kb_return_to_apps: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_apps]])