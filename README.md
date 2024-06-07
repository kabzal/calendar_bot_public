# Телеграм-бот на aiogram3

Этот репозиторий содержит Телеграм-бота, созданного с использованием aiogram3, с базой данных PostgreSQL. Бот взаимодействует с базой данных асинхронно с помощью библиотеки asyncpg.

## Установка

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/kabzal/calendar_bot_public.git
    cd calendar_bot_public
    ```

2. **Создайте виртуальное окружение и активируйте его:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # В Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте базу данных PostgreSQL:**

    - Восстановите базу данных из файла бэкапа ```database_calendar_bot.backup``` в pgAdmin

    - Либо настройте базу данных вручную:
      - Необходимо в базе создать 2 таблицы: ```roles``` и ```appointments```.
      - В таблице ```roles``` поля ```user_id``` (integer), ```role``` (text), ```current_date``` (text).
      - В таблице appointments поля ```admin``` (integer), ```client``` (integer), ```app_date``` (text), ```app_time``` (text), ```type``` (text), ```state``` (text), ```name``` (text), ```phone``` (text)

## Конфигурация

1. **Создайте файл `.env`:**

    Создайте файл ```.env``` и заполните его по примеру ```.env.example```.

    Пример содержимого `.env`:

    ```ini
    BOT_TOKEN='6257468896:AAEa-RGWdcLq5LavBWG_hMSf36Nm1Eh8oiu'

    user='your_user'
    password='your_password'
    database='your_database_name'
    host='your_host'
    ```
    Токен вашего бота необходимо получить через ```@BotFather``` в Telegram.
   
## Использование

1. **Запустите бота:**

    ```bash
    python bot.py
    ```

    Убедитесь, что сервер PostgreSQL запущен и доступен с учетными данными, указанными в файле `.env`.

2. **Перейдите в вашего бота в Telegram**
   Это демонстрационный бот, предоставляющий возможность протестировать функционал и с позиции клиента, и с позиции эксперта/админа.
   Чтобы оценить весь функционал, рекомендуется следующая последвоательность действий:

   1. Нажмите ```/start``` и с помощью инлайн-кнопки выберите роль "Эксперт".
   2. В новом меню выберите инлайн-кнопку "Мой календарь", откроется календарь на текущйи месяц. Выберите любой день.
   3. В начале день будет пустой. Вы как эксперт можете добавить свободные часы для записи в этот день. Для этого нажмите "Добавить", после чего введите время. После сообщения об успешном добавлении записи нажмите на кнопку "Вернуться": теперь в этом дне отражается свободное окно для записи. Добавьте еще 2-3 окна для записи.
   4. При желании вы можете нажать на одно из созданных окон для записи и выбрать там кнопку "Удалить", чтобы удалить его.
   5. Далее, находясь в расписании на определенный день, рекомендуем нажать "Вернуться", чтобы снова попасть в календарь, а затем "Назад", чтобы попасть в стартовое меню. Теперь вы можете выбрать "Изменить роль", чтобы испытать функционал клиента.
   6. Выбрав клиента, нажмите "Записаться". Откроется календарь. Выберите дату, в которой вы ранее создавали окна для записи.
   7. Выберите любое доступное время для записи. После этого следуйте инструкциям бота: введите ФИО и номер телефона

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл [LICENSE](LICENSE) для получения подробной информации.