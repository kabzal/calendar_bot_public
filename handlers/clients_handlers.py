from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from datetime import date, datetime
from filters.filters import IsClientCall, IsValidDate, IsAppData
from lexicon.lexicon_clients import LEX_CLIENTS_MESSAGES
from sql_requests.sql_requests import show_appointments, show_free_times, show_the_appointment, cancel_appointment
from keyboards.kb_total import kb_clients_appointments
from keyboards.kb_clients import kb_main_client, kb_free_times, kb_ok_cancel_func, kb_return_to_apps

router: Router = Router()
router.callback_query.filter(IsClientCall())  # Фильтр на коллбэки от клиентов


# Просмотр своих записей клиентом
@router.callback_query(Text(text='my_appointments'))
async def show_clients_appointments(callback: CallbackQuery):
    list_of_apps = await show_appointments(callback.from_user.id)  # Выгружаем записи из БД по id клиента
    kb_clients_appointments_builder = await kb_clients_appointments(list_of_apps)
    if list_of_apps:
        await callback.message.edit_text(text='Ваши текущие записи к эксперту:',
                                         reply_markup=kb_clients_appointments_builder.as_markup())
    else:
        await callback.message.edit_text(text='У вас пока нет ни одной записи 🤷‍♂',
                                         reply_markup=kb_clients_appointments_builder.as_markup())


# Кнопка "назад"
@router.callback_query(Text(text='back_to_begining'))
async def back_to_clients_beginning(callback: CallbackQuery):
    await callback.message.edit_text(LEX_CLIENTS_MESSAGES['start_message'],
                                     reply_markup=kb_main_client)


# Хэндер после выбора даты в календаре
@router.callback_query(IsValidDate())  # Применен фильтр на корректные даты
async def date_chosen(callback: CallbackQuery, dates_list: list[int]):
    current_date = str(date(day=dates_list[0], month=dates_list[1], year=dates_list[2])) # Дата в строку
    free_times = await show_free_times(callback.from_user.id, current_date)  # Выгрузка из БД свободных окон для записи
    kb_free_times_builder = await kb_free_times(free_times, current_date)  # Клавиатура с свободными окнами
    if free_times:
        await callback.message.edit_text(text='Выберите удобное время:',
                                         reply_markup=kb_free_times_builder.as_markup())
    else:
        await callback.message.edit_text(text='Кажется, в этот день нет свободных часов для записи',
                                         reply_markup=kb_free_times_builder.as_markup())


# Хэндлер при открытии конкретной записи
@router.callback_query(IsAppData())
async def app_opened(callback: CallbackQuery, app_data: list[str]):
    app_date = app_data[2]  # Берем из коллбэка дату
    app_time = app_data[1]  # Берем из коллбэка время

    # Выгружаем из БД данные о записи по id юзера, дате и времени:
    the_appointment = await show_the_appointment(user_id=callback.from_user.id, app_date=app_date, app_time=app_time)

    # Преобразуем дату в нужный формат:
    formatted_date = datetime.strftime(datetime.strptime(app_date, "%Y-%m-%d"), "%d.%m.%Y")

    # Кнопка "Отменить запись":
    kb_ok_cancel = (await kb_ok_cancel_func(current_date=app_date, current_time=app_time))[0]


    await callback.message.edit_text(text='Вы записаны к эксперту\n'
                                        f'на <b>{formatted_date}</b> в <b>{app_time}</b>\n\n'
                                        '<b>Стоимость консультации</b>: 1000 рублей\n\n'
                                        'Ваши данные:\n'
                                        f'<b>ФИО</b>: {the_appointment[0][3]}\n'
                                        f'<b>Телефон</b>: {the_appointment[0][4]}\n\n'
                                        'Если у Вас возникли планы, Вы можете '
                                        'отменить запись. Для этого нажмите кнопку '
                                        '<b>"Отменить запись"</b>', reply_markup=kb_ok_cancel)


# Функции для проверки коллбэков
def check_cancel_app(callback: CallbackQuery):
    return callback.data.startswith('cancel_app')


def check_sure_cancel_app(callback: CallbackQuery):
    return callback.data.startswith('sure_cancel_app')


# Хэндлер для запроса подтверждения отмены записи
@router.callback_query(check_cancel_app)
async def client_cancel_app(callback: CallbackQuery):
    app_date = callback.data.split()[1]  # Берем из коллбэка дату
    app_time = callback.data.split()[2]  # Берем из коллбэка время

    kb_sure_cancel = (await kb_ok_cancel_func(current_date=app_date, current_time=app_time))[1]
    await callback.message.edit_text(text='Вы уверены, что хотите отменить запись?', reply_markup=kb_sure_cancel)


# Хэндлер для отмены записи
@router.callback_query(check_sure_cancel_app)
async def client_sure_cancel_app(callback: CallbackQuery):
    app_date = callback.data.split()[1]  # Берем из коллбэка дату
    app_time = callback.data.split()[2]  # Берем из коллбэка время

    # Отменяем запись в БД
    await cancel_appointment(user_id=callback.from_user.id, app_date=app_date, app_time=app_time)

    await callback.message.edit_text(text='Запись успешно отменена.', reply_markup=kb_return_to_apps)
