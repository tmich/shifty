from fastapi import FastAPI
from sqlmodel import SQLModel
from shifty.api.routers import availabilities, shifts
from shifty.infrastructure.db import admin_engine

SQLModel.metadata.create_all(admin_engine)

app = FastAPI()
app.include_router(availabilities.router)
app.include_router(shifts.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}