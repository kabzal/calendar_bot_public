from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from filters.filters import IsValidFSM, IsValidSNP, IsClientMess
from lexicon.lexicon_clients import LEX_CLIENTS_MESSAGES
from sql_requests.sql_requests import create_appointment
from keyboards.kb_clients import kb_return_to_calendar

router: Router = Router()
router.message.filter(IsClientMess())

storage: MemoryStorage = MemoryStorage()

client_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMClient(StatesGroup):
    fill_snp = State()
    fill_phone = State()

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Запись прервана, чтобы вернуться в календарь, нажмите на кнопку "Вернуться в календарь"', reply_markup=kb_return_to_calendar)

@router.message(Command(commands='cancel'))
async def not_cancel_process(message: Message):
    await message.answer(text='Отменять нечего')

@router.callback_query(IsValidFSM(), StateFilter(default_state))
async def startFSM(callback: CallbackQuery, appointment_data: list[str], state: FSMContext):
    current_date = appointment_data[2]
    current_time = appointment_data[1]
    await state.update_data(current_date=current_date)
    await state.update_data(current_time=current_time)
    await callback.message.edit_text(text=LEX_CLIENTS_MESSAGES['anketa_nsp'])
    await state.set_state(FSMClient.fill_snp)

@router.message(StateFilter(FSMClient.fill_snp), IsValidSNP())
async def fill_phone_process(message: Message, state: FSMContext):
    await state.update_data(snp=message.text)
    await message.answer(text=LEX_CLIENTS_MESSAGES['anketa_mob_number'])
    await state.set_state(FSMClient.fill_phone)

@router.message(StateFilter(FSMClient.fill_snp))
async def warning_fill_snp(message: Message):
    await message.answer(text='ФИО введено некорректно. Попробуйте еще раз! Если хотите прекратить запись, нажмите /cancel')


def right_phone_check(message: Message):
    return message.text.isdigit() and len(message.text) == 11

@router.message(StateFilter(FSMClient.fill_phone), right_phone_check)
async def success_registration(message: Message, state: FSMClient):
    await state.update_data(phone=message.text)
    client_dict = {}
    client_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await create_appointment(user_id=message.from_user.id,
                             app_date=client_dict[message.from_user.id]['current_date'],
                             app_time=client_dict[message.from_user.id]['current_time'],
                             name=client_dict[message.from_user.id]['snp'],
                             phone=client_dict[message.from_user.id]['phone'])
    client_dict = {}
    await message.answer(text=LEX_CLIENTS_MESSAGES['successful_reg'], reply_markup=kb_return_to_calendar)

@router.message(StateFilter(FSMClient.fill_phone))
async def warning_fill_phone(message: Message):
    await message.answer(text='Номер телефона введен некорректно. Попробуйте еще раз.')