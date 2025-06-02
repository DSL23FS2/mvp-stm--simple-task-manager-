# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from nicegui import ui
import uvicorn
import sys
from pathlib import Path

from data.base_metadata import create_all
from data.models.task.api import router as task_api
from lib.ui import MainUI

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

app = FastAPI()

@ui.page('/')
def home():
    main_ui = MainUI()
    main_ui.create()

def main():
    # Инициализация базы данных
    create_all()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация маршрутов API
    app.include_router(task_api)

    # Запуск NiceGUI с FastAPI
    ui.run_with(app=app)
    
    # Запуск FastAPI с Uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

if __name__ == "__main__":
    main()