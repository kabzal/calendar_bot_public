from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime


# Стартовая клавиатура админа
cal: InlineKeyboardButton = InlineKeyboardButton(text='Мой календарь',
                                                 callback_data='show_calendar')
my_clients: InlineKeyboardButton = InlineKeyboardButton(text='Мои записи',
                                                        callback_data='my_clients')
new_role: InlineKeyboardButton = InlineKeyboardButton(text='Изменить роль',
                                                      callback_data='change_my_role')
kb_main_admin: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[cal], [my_clients], [new_role]])


# Функция, которая создает инлайн-кнопки со всеми записями в заданный день
async def kb_all_times(all_times: list, current_date):
    kb_all_times_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    b_all_times = []
    all_times = sorted(all_times, key=lambda x: x[1])
    for time in all_times:
        if time[3] == 'free':
            b_all_times.append(InlineKeyboardButton(text=(f'{time[1]} - 🟢'),
                                                    callback_data=(f'all_times {time[1]} {current_date} {time[3]}')))
        elif time[3] == 'appointment':
            b_all_times.append(InlineKeyboardButton(text=(f'{time[1]} - 🔴'),
                                                    callback_data=(f'all_times {time[1]} {current_date} {time[3]}')))
    b_all_times.append(InlineKeyboardButton(text='Добавить',
                                            callback_data='add_new_appoint'))
    b_all_times.append(InlineKeyboardButton(text='Вернуться',
                                            callback_data='show_calendar'))
    kb_all_times_builder.row(*b_all_times, width=1)
    return kb_all_times_builder

# Клавиатура с кнопкой "Назад в календарь"
return_to_calendar: InlineKeyboardButton = InlineKeyboardButton(text='Назад в календарь',
                                                                callback_data='show_calendar')
kb_return_to_calendar: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_calendar]])


# Функция, которая передает информацию о дате и времени в хендлер для отмены записи админом
async def kb_ok_cancel_func(current_date, current_time):
    okey: InlineKeyboardButton = InlineKeyboardButton(text='Назад к списку',
                                                      callback_data='my_clients')
    cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись',
                                                        callback_data=('cancel_app' + ' ' + str(current_date) + ' ' + str(current_time)))
    sure_cancel: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись',
                                                             callback_data=('sure_cancel_app'+ ' ' + str(current_date) + ' ' + str(current_time)))
    kb_ok_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okey, cancel]])
    kb_sure_cancel: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[okey, sure_cancel]])
    return [kb_ok_cancel, kb_sure_cancel]

# Клавиатура с кнопкой "Назад в мои записи"
return_to_clients: InlineKeyboardButton = InlineKeyboardButton(text='Назад в мои записи', callback_data='my_clients')
kb_return_to_clients: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_clients]])


# Функция для формирования двух клавиатур:
# Клавиатура 1: удаление окна записи и возврат
# Клавиатура 2: возврат (если нет окон записи для удаления)
async def kb_delete_free_time_func(current_date, current_time):
    new_format_date = datetime.strftime(datetime.strptime(current_date, "%Y-%m-%d"), "%d:%m:%Y")
    delete_free_time: InlineKeyboardButton = InlineKeyboardButton(text='Удалить', callback_data=f'delete_free_time={current_time}={current_date}')
    return_to_date: InlineKeyboardButton = InlineKeyboardButton(text='Вернуться', callback_data=new_format_date)
    kb_delete_free_time: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[delete_free_time], [return_to_date]])
    kb_free_time_deleted: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_date]])
    return [kb_delete_free_time, kb_free_time_deleted]


# Функция для формирования двух клавиатур:
# Клавиатура 1: отмена записи и возврат
# Клавиатура 2: подтверждение отмены записи и возврат
async def kb_cancel_app_from_calendar(current_date, current_time):
    new_format_date = datetime.strftime(datetime.strptime(current_date, "%Y-%m-%d"), "%d:%m:%Y")
    cancel_from_calendar: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись', callback_data=f'cancel_app_from_calendar' + ' ' + str(current_date) + ' ' + str(current_time))
    sure_cancel_from_calendar: InlineKeyboardButton = InlineKeyboardButton(text='Отменить запись', callback_data=f'sure_cancel_app_from_calendar' + ' ' + str(current_date) + ' ' + str(current_time))
    return_to_date: InlineKeyboardButton = InlineKeyboardButton(text='Вернуться', callback_data=new_format_date)
    kb_ok_cancel_from_calendar: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_date, cancel_from_calendar]])
    kb_sure_cancel_from_calendar: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[return_to_date, sure_cancel_from_calendar]])
    return [kb_ok_cancel_from_calendar, kb_sure_cancel_from_calendar]
