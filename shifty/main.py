from fastapi import FastAPI
from sqlmodel import SQLModel
from shifty.api.routers import availabilities
from shifty.infrastructure.db import engine

SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(availabilities.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}