from data import DatabaseInitializer;
from data.models.task.api import route_api
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI;

app = FastAPI();

def main():
    # Инициализация базы данных
    db = DatabaseInitializer();
    db.create_all();  # Создание всех таблиц в базе данных

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить все источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешить все методы
        allow_headers=["*"],  # Разрешить все заголовки
    )

    # Регистрация маршрутов API
    session = db.get_session()  # Получение сессии SQLAlchemy
    app.include_router(route_api(session))  # Регистрация маршрутов задач
    
    # Запуск приложения FastAPI
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

if __name__ == "__main__":
    main()