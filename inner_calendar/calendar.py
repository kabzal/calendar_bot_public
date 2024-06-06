import calendar
from datetime import date
from aiogram import Router
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sql_requests.sql_requests import change_user_date, show_user_date

#создаем роутер
router: Router = Router()

#функция, которая будет создавать клавиатуру в виде календаря
async def calendar_made_here(current_year, current_month):
    month_names = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
                   5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                   9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',}
    calendar_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    #Кнопки
    b_back = InlineKeyboardButton(text='<<', callback_data='back')
    b_forward = InlineKeyboardButton(text='>>', callback_data='forward')
    b_year = InlineKeyboardButton(text=current_year, callback_data='ignore')
    b_month = InlineKeyboardButton(text=month_names[current_month], callback_data='ignore')
    b_return = InlineKeyboardButton(text='Назад', callback_data='back_to_begining')

    calendar_list = calendar.monthcalendar(current_year, current_month)

    b_days: list[InlineKeyboardButton] = []

    for week in calendar_list:
        for day in week:
            if int(day) == 0:
                b_days.append(InlineKeyboardButton(text=str(' '), callback_data='ignore'))
            else:
                b_days.append(InlineKeyboardButton(text=str(day), callback_data=(str(day)+':'+str(current_month)+':'+str(current_year))))
    calendar_builder.add(b_month)
    calendar_builder.row(*b_days, width=7)
    calendar_builder.row(*[b_back, b_year, b_forward], width=3)
    calendar_builder.row(*[b_return], width=1)
    return calendar_builder



#Хэндлер, который выдает календарь по команде календарь
@router.callback_query(Text(text='show_calendar'))
async def give_calendar(callback: CallbackQuery):
    await change_user_date(user_id=callback.from_user.id, cur_date=str(date.today())) #Сохраняем в БД текущую дату
    current_day = str(date.today()).split('-')
    current_year = int(current_day[0])
    current_month = int(current_day[1])
    calendar_builder = await calendar_made_here(current_year, current_month)
    await callback.message.edit_text(text='Выберите интересующую Вас дату:', reply_markup=calendar_builder.as_markup())

#Хэндлер, который листает вперед
@router.callback_query(Text(text='forward'))
async def forward_calendar(callback: CallbackQuery):
    current_date = await show_user_date(callback.from_user.id)
    #Сохраняем в БД новую дату
    if current_date[1] == 12:
        await change_user_date(user_id=callback.from_user.id, cur_date=str(date(year=current_date[0]+1, month=1, day=1)))
    else:
        await change_user_date(user_id=callback.from_user.id, cur_date=str(date(year=current_date[0], month=current_date[1]+1, day=1)))
    new_date = await show_user_date(callback.from_user.id)
    current_year = new_date[0]
    current_month = new_date[1]
    calendar_builder = await calendar_made_here(current_year, current_month)
    await callback.message.edit_text(text='Выберите интересующую Вас дату:', reply_markup=calendar_builder.as_markup())

#Хэндлер, который листает назад
@router.callback_query(Text(text='back'))
async def back_calendar(callback: CallbackQuery):
    current_date = await show_user_date(callback.from_user.id)
    #Сохраняем в БД новую дату
    if current_date[1] == 1:
        await change_user_date(user_id=callback.from_user.id, cur_date=str(date(year=current_date[0]-1, month=12, day=1)))
    else:
        await change_user_date(user_id=callback.from_user.id, cur_date=str(date(year=current_date[0], month=current_date[1]-1, day=1)))
    new_date = await show_user_date(callback.from_user.id)
    current_year = new_date[0]
    current_month = new_date[1]
    calendar_builder = await calendar_made_here(current_year, current_month)
    await callback.message.edit_text(text='Выберите интересующую Вас дату:', reply_markup=calendar_builder.as_markup())