import asyncpg
from config_data.config import Config, load_config


# Данные для подклчения к БД
config: Config = load_config()
user=config.db.user
password=config.db.password
database=config.db.database
host=config.db.host


# Функция для внесения сведений о роли юзера в БД roles
async def appoint_user_role(user_id, user_role, cur_date):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO roles (user_id, role, "current_date")'''
                       '''VALUES ($1, $2, $3)''', user_id, user_role, cur_date)
    await conn.close()


# Функция для проверки юзера в БД roles
async def check_user(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    check = await conn.fetchval('''SELECT EXISTS (SELECT * FROM roles WHERE user_id=$1)''', user_id)
    await conn.close()
    return str(check)


# Функция для изменения роли юзера в БД roles
async def change_user_role(user_id, user_role):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''UPDATE roles SET role = $2 WHERE user_id = $1''', user_id, user_role)
    await conn.close()


# Функция для изменения даты юзера в БД roles
async def change_user_date(user_id, cur_date):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''UPDATE roles SET "current_date" = $2 WHERE user_id = $1''', user_id, cur_date)
    await conn.close()


# Функция для вывода из БД текущей роли юзера
async def show_user_role(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    current_role = await conn.fetchval('''SELECT role FROM roles WHERE user_id=$1''', user_id)
    await conn.close()
    return current_role


# Функция для вывода из БД текущей даты юзера
async def show_user_date(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    current_date = await conn.fetchval(f'''SELECT "current_date" FROM roles WHERE user_id=$1''', user_id)
    await conn.close()
    return [int(i) for i in str(current_date).split('-')]


# Создание нового свободного часа в определенный день в таблице appointments
async def new_time(user_id, app_date, app_time, app_state):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO appointments (admin, app_date, app_time, state)'''
                       '''VALUES ($1, $2, $3, $4)''', user_id, app_date, app_time, app_state)
    await conn.close()


# Функция для удаления даты и времени в БД appointments
async def delete_time(user_id, app_date, app_time):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''DELETE FROM appointments WHERE admin=$1 AND app_date=$2 AND app_time=$3''', user_id, app_date, app_time)
    await conn.close()


# Функция для создания записи в БД appointments
async def create_appointment(user_id, app_date, app_time, name, phone):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute("UPDATE appointments SET client=$1, name=$2, phone=$3, state='appointment'"
                       "WHERE admin=$4 AND app_date=$5 AND app_time=$6", user_id, name, phone, user_id, app_date, app_time)
    await conn.close()


# Функция для отмены записи в БД appointments
async def cancel_appointment(user_id, app_date, app_time):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute("UPDATE appointments SET client=null, type=null, name=null, phone=null, state='free'"
                       " WHERE admin=$1 AND app_date=$2 AND app_time=$3", user_id, app_date, app_time)
    await conn.close()


# Функция для вывода данных о свободном времени в БД appointments
async def show_free_times(user_id, app_date):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    times = await conn.fetch("SELECT app_time FROM appointments WHERE admin=$1 AND app_date=$2 AND state='free'", user_id, app_date)
    await conn.close()
    return [time['app_time'] for time in times]


# Функция для вывода данных о записях в БД appointments
async def show_appointments(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    apps = await conn.fetch("SELECT app_date, app_time, type, name, phone FROM appointments WHERE admin=$1 AND state='appointment'", user_id)
    await conn.close()
    return [[app['app_date'], app['app_time'], app['type'], app['name'], app['phone']] for app in apps]


# Функция для вывода данных о любом времени в БД appointments
async def show_all(user_id, app_date):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    alls = await conn.fetch("SELECT app_date, app_time, type, state, name, phone FROM appointments WHERE admin=$1 AND app_date=$2", user_id, app_date)
    await conn.close()
    return [[all['app_date'], all['app_time'], all['type'], all['state'], all['name'], all['phone']] for all in alls]


# Функция для проверки, не занято ли время в БД appointments
async def free_time_question(user_id, app_date, app_time):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    check_time = await conn.fetchval('SELECT EXISTS (SELECT * FROM appointments WHERE admin=$1 AND app_date=$2 AND app_time=$3)', user_id, app_date, app_time)
    await conn.close()
    return str(check_time)


# Функция для выгрузки списка данных о записях
async def show_the_appointment(user_id, app_date, app_time):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    apps = await conn.fetch("SELECT app_date, app_time, type, name, phone FROM appointments WHERE admin=$1 AND state='appointment' AND app_date=$2 AND app_time=$3", user_id, app_date, app_time)
    await conn.close()
    return [[app['app_date'], app['app_time'], app['type'], app['name'], app['phone']] for app in apps]
