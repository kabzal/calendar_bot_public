from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from datetime import date, datetime

from filters.filters import IsAdminCall, IsValidDate, IsAppData, IsAdminMess
from lexicon.lexicon_admin import LEX_ADMIN_MESSAGES
from sql_requests.sql_requests import show_appointments, show_all, change_user_date, show_the_appointment, cancel_appointment, delete_time
from keyboards.kb_total import kb_clients_appointments
from keyboards.kb_admin import kb_main_admin, kb_all_times, kb_ok_cancel_func, kb_return_to_clients, kb_delete_free_time_func, kb_cancel_app_from_calendar

router: Router = Router()
# Фильтры на коллбэки и сообщения от админа
router.callback_query.filter(IsAdminCall())
router.message.filter(IsAdminMess())


# Открывается список актуальных записей
@router.callback_query(Text(text='my_clients'))
async def show_admin_appointments(callback: CallbackQuery):
    list_of_apps = await show_appointments(callback.from_user.id)
    if list_of_apps:
        kb_admin_appointments_builder = await kb_clients_appointments(list_of_apps)
        await callback.message.edit_text(text='Записи к вам',
                                         reply_markup=kb_admin_appointments_builder.as_markup())
    else:
        kb_admin_appointments_builder = await kb_clients_appointments(list_of_apps)
        await callback.message.edit_text(text='К вам пока нет ни одной записи',
                                         reply_markup=kb_admin_appointments_builder.as_markup())


# Возврат в стартовое меню админа
@router.callback_query(Text(text='back_to_begining'))
async def back_to_admin_beginning(callback: CallbackQuery):
    await callback.message.edit_text(text=LEX_ADMIN_MESSAGES['start_message'],
                                     reply_markup=kb_main_admin)


# Выбрана дата в календаре, высвечиваются свободные и занятые часы
@router.callback_query(IsValidDate())
async def date_chosen(callback: CallbackQuery, dates_list: list[int]):

    # Определяем и сохраняем выбранную дату
    current_date = str(date(day=dates_list[0], month=dates_list[1], year=dates_list[2]))
    await change_user_date(user_id=callback.from_user.id, cur_date=current_date)

    # Выгружаем и выдаем список свободных окон и забронированных записей в выбранную дату
    all_times = await show_all(callback.from_user.id, current_date)
    kb_all_times_builder = await kb_all_times(all_times, current_date)

    if all_times:
        await callback.message.edit_text(text='Выберите время:\n\n🟢 - это время свободно\n🔴 - на это время есть запись', reply_markup=kb_all_times_builder.as_markup())
    else:
        await callback.message.edit_text(text='Часы для записи в этот день не добавлены', reply_markup=kb_all_times_builder.as_markup())


# Выбрана какая-нибудь бронь (запись клиента)
@router.callback_query(IsAppData())
async def app_opened(callback: CallbackQuery, app_data: list[str]):
    app_date = app_data[2]  # Из коллбэка выгружается дата
    app_time = app_data[1]  # Из коллбэка выгружается время

    # Выгружается запись из БД по дате и времени
    the_appointment = await show_the_appointment(user_id=callback.from_user.id, app_date=app_date, app_time=app_time)
    formatted_date = datetime.strftime(datetime.strptime(app_date, "%Y-%m-%d"), "%d.%m.%Y")

    # Выдаем инфо о записи и клавиатуру с действиями
    kb_ok_cancel = (await kb_ok_cancel_func(current_date=app_date, current_time=app_time))[0]
    await callback.message.edit_text(text='К вам запись\n'
                                        f'на {formatted_date} в {app_time}\n\n'
                                        '<b>Стоимость консультации</b>: 1000 рублей\n\n'
                                        'Данные клиента:\n'
                                        f'ФИО: {the_appointment[0][3]}\n'
                                        f'Телефон: {the_appointment[0][4]}\n\n'
                                        'Если у Вас другие планы, Вы можете '
                                        'отменить запись. Для этого нажмите кнопку '
                                        '"Отменить запись"', reply_markup=kb_ok_cancel)


def check_cancel_app(callback: CallbackQuery):
    return callback.data.startswith('cancel_app ')


def check_sure_cancel_app(callback: CallbackQuery):
    return callback.data.startswith('sure_cancel_app ')


@router.callback_query(check_cancel_app)
async def client_cancel_app(callback: CallbackQuery):
    app_date = callback.data.split()[1]
    app_time = callback.data.split()[2]
    kb_sure_cancel = (await kb_ok_cancel_func(current_date=app_date, current_time=app_time))[1]
    await callback.message.edit_text(text=('Вы уверены, что хотите отменить запись?'), reply_markup=kb_sure_cancel)


@router.callback_query(check_sure_cancel_app)
async def client_sure_cancel_app(callback: CallbackQuery):
    app_date = callback.data.split()[1]
    app_time = callback.data.split()[2]
    await cancel_appointment(user_id=callback.from_user.id, app_date=app_date, app_time=app_time)
    await callback.message.edit_text(text='Запись успешно отменена.', reply_markup=kb_return_to_clients)


def all_time_chosen(callback: CallbackQuery):
    return callback.data.startswith('all_times')


# В календаре в определенный день выбрана свободная или занятая запись
@router.callback_query(all_time_chosen)
async def admin_chose_all_times(callback: CallbackQuery):
    app_date = callback.data.split()[2]
    app_time = callback.data.split()[1]
    free_or_app = callback.data.split()[3]
    if free_or_app == 'free':
        kb_delete_free_time = (await kb_delete_free_time_func(app_date, app_time))[0]
        await callback.message.edit_text(text=f'В этот день в {app_time} свободно. Чтобы удалить это время из календаря, нажмите "Удалить"', reply_markup=kb_delete_free_time)
    elif free_or_app == 'appointment':
        the_appointment = await show_the_appointment(user_id=callback.from_user.id, app_date=app_date, app_time=app_time)
        formatted_date = datetime.strftime(datetime.strptime(app_date, "%Y-%m-%d"), "%d.%m.%Y")
        kb_ok_cancel = (await kb_cancel_app_from_calendar(current_date=app_date, current_time=app_time))[0]
        await callback.message.edit_text(text='К вам запись\n'
                                            f'на {formatted_date} в {app_time}\n\n'
                                            '<b>Стоимость консультации</b>: 1000 рублей\n\n'
                                            'Данные клиента:\n'
                                            f'ФИО: {the_appointment[0][3]}\n'
                                            f'Телефон: {the_appointment[0][4]}\n\n'
                                            'Если у Вас другие планы, Вы можете '
                                            'отменить запись. Для этого нажмите кнопку '
                                            '"Отменить запись"', reply_markup=kb_ok_cancel)


def del_free_time_chosen(callback: CallbackQuery):
    return callback.data.startswith('delete_free_time')


# Удаление свободного окна для записи
@router.callback_query(del_free_time_chosen)
async def delete_free_time_process(callback: CallbackQuery):
    current_date = callback.data.split('=')[2]
    current_time = callback.data.split('=')[1]
    await delete_time(user_id=callback.from_user.id, app_date=current_date, app_time=current_time)
    kb_free_time_deleted = (await kb_delete_free_time_func(current_date, current_time))[1]
    await callback.message.edit_text(text='Время удалено.', reply_markup=kb_free_time_deleted)


def check_cancel_app_from_calendar(callback: CallbackQuery):
    return callback.data.startswith('cancel_app_from_calendar')


def check_sure_cancel_app_from_calendar(callback: CallbackQuery):
    return callback.data.startswith('sure_cancel_app_from_calendar')


# Запрос подтверждения отмены записи
@router.callback_query(check_cancel_app_from_calendar)
async def client_cancel_app(callback: CallbackQuery):
    app_date = callback.data.split()[1]
    app_time = callback.data.split()[2]
    kb_sure_cancel = (await kb_cancel_app_from_calendar(current_date=app_date,
                                                        current_time=app_time))[1]
    await callback.message.edit_text(text='Вы уверены, что хотите отменить запись?',
                                     reply_markup=kb_sure_cancel)


# Отмена записи после подтверждения
@router.callback_query(check_sure_cancel_app_from_calendar)
async def client_sure_cancel_app(callback: CallbackQuery):
    current_date = callback.data.split()[1]
    current_time = callback.data.split()[2]
    kb_app_deleted = (await kb_delete_free_time_func(current_date, current_time))[1]
    await cancel_appointment(user_id=callback.from_user.id,
                             app_date=current_date,
                             app_time=current_time)
    await callback.message.edit_text(text='Запись успешно отменена.',
                                     reply_markup=kb_app_deleted)
