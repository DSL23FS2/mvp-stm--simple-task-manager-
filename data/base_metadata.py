# Метаданные базы данных
# data/database_base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base();

class DatabaseInitializer:
    def __init__(self, db_url: str = 'sqlite:///tasks.db'):
        self.engine = create_engine(db_url) # создание подключения к БД
        self.Session = sessionmaker(bind=self.engine) # создание фабрики сессии

    # Создание всех новых таблиц в метаданных. 
    # Уже созданные таблицы не затрагиваются, т.к. не изменяются методанные.
    def create_all(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()