from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    user: str          # Username пользователя базы данных
    password: str      # Пароль к базе данных
    database: str      # Название базы данных
    host: str          # URL-адрес базы данных

@dataclass
class TgBot:
    token: str    # Токен для доступа к телеграм-боту

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                    token=env('BOT_TOKEN')),
                    db=DatabaseConfig(user=env('user'),
                                      password=env('password'),
                                      database=env('database'),
                                      host=env('host')))