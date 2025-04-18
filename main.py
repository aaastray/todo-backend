import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import engine
from src.init_db import init_db
from src.routers.todo import todo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)

@app.on_event("startup")
async def startup():
    print('Приложение запускается...')
    await init_db(engine)
    print('База данных инициализирована.')