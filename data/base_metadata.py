# Метаданные базы данных
# data/database_base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base();

# URL подключения к базе данных
db_url = 'sqlite:///tasks.db'
engine = create_engine(db_url) # создание подключения к БД
Session = sessionmaker(bind=engine) # создание фабрики сессии

def create_all():
    Base.metadata.create_all(engine)

def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()