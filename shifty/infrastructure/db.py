import os
from typing import Generator
from fastapi import Depends
from sqlalchemy import Connection
from sqlmodel import Session, create_engine, text
from shifty.security.dependencies import get_current_user_id
from shifty.infrastructure.functions import all_functions
from shifty.infrastructure.security_policies import all_policies
from shifty.infrastructure.roles import all_roles


# create a new postgresql database
admin_engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres@localhost:5431/{os.getenv('SHIFTY_DB', 'shiftydb')}",
    isolation_level="READ UNCOMMITTED",  # Use READ UNCOMMITTED to avoid locking issues during schema changes
    echo=True,  # Enable SQLAlchemy logging
    future=True,  # Use future=True for SQLModel compatibility
)
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('SHIFTY_USER', 'shifty_user')}:{os.getenv('SHIFTY_PASSWORD', 'pwd')}@localhost:5431/{os.getenv('SHIFTY_DB', 'shiftydb')}",
    isolation_level="READ UNCOMMITTED",  # Use READ UNCOMMITTED to avoid locking issues during schema changes
    echo=True,  # Enable SQLAlchemy logging
    future=True,  # Use future=True for SQLModel compatibility
)

# Disable the "sane rowcount" feature for psycopg2
# This is necessary because psycopg2 does not support the `RETURNING` clause in all cases
# source: https://groups.google.com/g/sqlalchemy/c/WA-E1pyCeD0?pli=1
engine.dialect.supports_sane_rowcount = False


# Dipendenza FastAPI
def get_admin_session() -> Generator[Session, None, None]:
    with Session(admin_engine) as db:
        try:
            yield db
        finally:
            db.close()


def get_session(
    user_id: str = Depends(get_current_user_id),
) -> Generator[Session, None, None]:
    with Session(engine) as db:
        try:
            # Set the current user ID for RLS
            db.connection().execute(text(f"SET app.current_user_id = '{user_id}'"))
            yield db
        finally:
            # Reset the current user ID after the request
            # This is important to avoid leaking user context between requests
            db.connection().execute(text("RESET app.current_user_id"))
            db.close()


def create_all_functions(conn: Connection):
    for function in all_functions:
        conn.execute(function)
    conn.commit()
    
def create_all_security_policies(conn: Connection):
    for policy in all_policies:
        conn.execute(policy)
    conn.commit()

def create_roles(conn: Connection):
    for role in all_roles:
        conn.execute(role)
    conn.commit()