from fastapi import Depends, FastAPI
from shifty.api.routers import availabilities
from shifty.dependencies import get_availability_service  # Updated import

app = FastAPI()
# app.include_router(availabilities.router, dependencies=[Depends(get_availability_service)])
app.include_router(availabilities.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}