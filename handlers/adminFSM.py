from datetime import date

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import StateFilter, Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from filters.filters import IsAdminMess, IsAdminCall, IsValidFreeTime
from keyboards.kb_admin import kb_delete_free_time_func
from lexicon.lexicon_admin import LEX_ADMIN_MESSAGES
from sql_requests.sql_requests import free_time_question, show_user_date, new_time
from keyboards.kb_clients import kb_return_to_calendar

router: Router = Router()
router.callback_query.filter(IsAdminCall())
router.message.filter(IsAdminMess())

storage: MemoryStorage = MemoryStorage()


# Создаем машину состояний для создания окна записи в определенное время
class FSMAdmin(StatesGroup):
    fill_time = State()


# Отмена: прерывание машины состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Создание окна записи прервано. '
                              'Чтобы вернуться в календарь, '
                              'нажмите на кнопку "Вернуться в календарь"',
                         reply_markup=kb_return_to_calendar)


# Отмена: когда клиент вне машины состояний
@router.message(Command(commands='cancel'))
async def not_cancel_process(message: Message):
    await message.answer(text='Отменять нечего')


# Вход в машину состояний: нажата кнопка Добавить (новое окно для записи)
@router.callback_query(Text(text='add_new_appoint'), StateFilter(default_state))
async def start_admin_FSM(callback: CallbackQuery, state: FSMContext):
    # Выдаем сообщение с просьбой ввести время и переходим в состояние ожидания ввода времени
    await callback.message.edit_text(text=LEX_ADMIN_MESSAGES['set_time_start'])
    await state.set_state(FSMAdmin.fill_time)


# Хэндлер при корректном вводе времени
@router.message(StateFilter(FSMAdmin.fill_time), IsValidFreeTime())
async def success_add_new_free_time(message: Message, state: FSMContext, times_list: list[str]):

    # Определяем выбранную дату
    current_date = await show_user_date(user_id=message.from_user.id)
    current_date = str(date(year=current_date[0], month=current_date[1], day=current_date[2]))

    # Проверяем введенное время на наличие в БД
    given_time = ':'.join(times_list)
    check = await free_time_question(user_id=message.from_user.id,
                                     app_date=current_date,
                                     app_time=given_time)
    if check == 'True': # Если в БД уже есть окно на это время
        await message.answer(text='На это время уже есть окно для записи. '
                                  'Попробуйте еще раз! '
                                  'Если хотите прекратить создание нового окна, '
                                  'нажмите /cancel')
    elif check == 'False': # Если в БД данное время не используется
        await new_time(user_id=message.from_user.id,
                       app_date=current_date,
                       app_time=given_time,
                       app_state='free')
        kb_return_to_date = (await kb_delete_free_time_func(current_date=current_date,
                                                            current_time=given_time))[1]
        await message.answer(text=LEX_ADMIN_MESSAGES['set_time_success'],
                             reply_markup=kb_return_to_date)
        await state.clear()


# Хэндлер при некорректном вводе времени
@router.message(StateFilter(FSMAdmin.fill_time))
async def warning_fill_time(message: Message):
    await message.answer(text='Вы ввели некорректное время. '
                              'Попробуйте еще раз! '
                              'Если хотите прекратить создание нового окна, '
                              'нажмите /cancel')
