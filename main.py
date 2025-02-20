from fastapi import FastAPI
from routes import employee_router
from db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("initializing Database")
    init_db()
    yield
    print("shutting down database")

app = FastAPI(lifespan=lifespan, title="Employee Management API")

app.include_router(employee_router)

@app.get('/')
async def home():
    return {"message": "Welcome to Employee Management API"}