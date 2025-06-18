from fastapi import FastAPI
from sqlmodel import SQLModel
from shifty.api.routers import availabilities, shifts, overrides, users, auth, registration
from shifty.infrastructure.db import (
    admin_engine, 
    create_all_functions,
    create_all_security_policies,
    create_roles
    )
from fastapi.middleware.cors import CORSMiddleware

# Create all tables in the database
# This will create the tables defined in the SQLModel models
SQLModel.metadata.create_all(admin_engine)

# Create roles, functions and security policies
with admin_engine.connect() as conn:
    create_all_functions(conn)
    create_all_security_policies(conn)
    create_roles(conn)

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
# Adjust the allowed origins as needed; for development, you might use "*" to allow all origins
# but it's better to specify the frontend URL for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers for different API endpoints
app.include_router(availabilities.router)
app.include_router(shifts.router)
app.include_router(overrides.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(registration.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}