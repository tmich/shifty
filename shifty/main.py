from fastapi import FastAPI
from sqlmodel import SQLModel
from shifty.api.routers import availabilities, shifts, overrides, users
from shifty.infrastructure.db import (
    admin_engine, 
    create_default_user, 
    create_function_current_organization_id, 
    create_function_current_role,
    create_availability_security_policies,
    create_user_security_policies,
    create_function_is_manager,
    create_function_is_admin
    )
from fastapi.middleware.cors import CORSMiddleware

# Create all tables in the database
# This will create the tables defined in the SQLModel models
SQLModel.metadata.create_all(admin_engine)

# Create default user, function for current organization ID, and security policies for availabilities
with admin_engine.connect() as conn:
    create_default_user(conn)
    create_function_current_organization_id(conn)
    create_function_current_role(conn)
    create_function_is_manager(conn)
    create_availability_security_policies(conn)
    create_user_security_policies(conn)
    create_function_is_admin(conn)
    conn.commit()

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

app.include_router(availabilities.router)
app.include_router(shifts.router)
app.include_router(overrides.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}