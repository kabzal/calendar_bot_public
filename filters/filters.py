from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sql_requests.sql_requests import show_user_role


# Фильтр: коллбэки админа
class IsAdminCall(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        role = await show_user_role(callback.from_user.id)
        return role == 'admin'


# Фильтр: коллбэки клиента
class IsClientCall(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        role = await show_user_role(callback.from_user.id)
        return role == 'client'


# Фильтр: сообщения админа
class IsAdminMess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        role = await show_user_role(message.from_user.id)
        return role == 'admin'


# Фильтр: сообщения клиента
class IsClientMess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        role = await show_user_role(message.from_user.id)
        return role == 'client'


# Фильтр: корректная дата
class IsValidDate(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, list[int]]:
        dates_list = []
        if callback.data.startswith('cancel_app') or callback.data.startswith('sure_cancel_app') or callback.data.startswith('all_times'):
            return False
        for d in callback.data.split(':'):
            if d.isdigit():
                dates_list.append(int(d))
        if dates_list:
            return {'dates_list': dates_list}
        return False


# Фильтр: корректное время
class IsValidFreeTime(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[str]]:
        times_list = []
        try:
            for t in message.text.split(':'):
                if t.isdigit():
                    times_list.append(t)
            if times_list and len(times_list) == 2 and 0 <= int(times_list[0]) <= 23 and 0 <= int(times_list[1]) <= 59:
                return {'times_list': times_list}
        except:
            return False


# Фильтр: если коллбэк startFSM, то передаем в хэндлер список
class IsValidFSM(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, list[str]]:
        appointment_data = []
        for a in callback.data.split():
            appointment_data.append(a)
        if appointment_data[0] == 'startFSM':
            return {'appointment_data': appointment_data}
        return False


# Фильтр: корректные ФИО
class IsValidSNP(BaseFilter):
    async def __call__(self, message: Message) -> bool | str:
        snp = []
        try:
            for s in message.text.split():
                if s.isalpha():
                    snp.append(s)
            if len(snp) == 3:
                return message.text
        except:
            return False


# Фильтр: если коллбэк app (запрос конкретной записи),
# Передаем в хэндлер данные о записи
class IsAppData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, list[str]]:
        app_data = []
        for app in callback.data.split():
            app_data.append(app)
        if app_data[0] == 'app':
            return {'app_data': app_data}
        return False
