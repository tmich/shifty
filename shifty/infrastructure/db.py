from contextlib import contextmanager
from typing import Generator
from fastapi import Depends
from sqlmodel import Session, create_engine, text
from shifty.security.dependencies import get_current_user_id

default_user = "shifty_user"
default_password = "shifty_password"
shiftydb = "shiftydb"

# create a new postgresql database
admin_engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres@localhost:5431/{shiftydb}",
    isolation_level="READ UNCOMMITTED",  # Use READ UNCOMMITTED to avoid locking issues during schema changes
    echo=True, # Enable SQLAlchemy logging
    future=True, # Use future=True for SQLModel compatibility
)
engine = create_engine(
    f"postgresql+psycopg2://{default_user}:{default_password}@localhost:5431/{shiftydb}",
    isolation_level="READ UNCOMMITTED",  # Use READ UNCOMMITTED to avoid locking issues during schema changes
    echo=True,  # Enable SQLAlchemy logging
    future=True, # Use future=True for SQLModel compatibility
)

# Disable the "sane rowcount" feature for psycopg2
# This is necessary because psycopg2 does not support the `RETURNING` clause in all cases
# source: https://groups.google.com/g/sqlalchemy/c/WA-E1pyCeD0?pli=1
engine.dialect.supports_sane_rowcount = False


# Dipendenza FastAPI
def get_session() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def get_db_with_rls(
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


# with admin_engine.connect() as connection:
def create_default_user(connection):
    query = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_roles
            WHERE  rolname = '{default_user}') 
        THEN
            CREATE ROLE {default_user} LOGIN PASSWORD '{default_password}';
        ELSE
            RAISE NOTICE 'Role "{default_user}" already exists. Skipping.';
        END IF;
    END $$;

    GRANT CONNECT ON DATABASE shiftydb TO {default_user};
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {default_user};
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {default_user};
    """
    connection.execute(text(query))
    connection.commit()


def create_function_current_organization_id(conn):
    # Function to get the current organization ID based on the user's organization membership
    create_function = text(
        """
    CREATE OR REPLACE FUNCTION public.current_organization_id()
     RETURNS uuid
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN (SELECT organization_id FROM user_organizations WHERE user_id = current_setting('app.current_user_id')::uuid);
    END; $function$
    ;
    """
    )

    conn.execute(create_function)


def create_availability_security_policies(conn):
    # Policy function for filtering rows based on organization membership
    availabilities_sel_policy = text(
        """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'availabilities_sel_policy') 
        THEN
            CREATE POLICY availabilities_sel_policy ON availabilities
            FOR SELECT
            USING (organization_id = current_organization_id());
        ELSE
            RAISE NOTICE 'Policy "availabilities_sel_policy" already exists. Skipping.';
        END IF;
    END $$;
    ;
    """
    )

    availabilities_ins_policy = text(
        """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'availabilities_ins_policy') 
        THEN
            CREATE POLICY availabilities_ins_policy ON availabilities
            FOR insert
            with check (
                user_id = current_setting('app.current_user_id')::uuid 
                OR 
                (
                    EXISTS (
                        SELECT 1 FROM users u
                        WHERE u.id = current_setting('app.current_user_id')::uuid
                        AND u.role IN('admin', 'manager')
                    )
                )
            );
        ELSE
            RAISE NOTICE 'Policy "availabilities_ins_policy" already exists. Skipping.';
        END IF;
    END $$;    
    """
    )

    availabilities_mod_policy = text(
        """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'availabilities_mod_policy') 
        THEN
            CREATE POLICY availabilities_mod_policy ON availabilities
            FOR update
            with check (
                user_id = current_setting('app.current_user_id')::uuid 
                OR 
                (
                    EXISTS (
                        SELECT 1 FROM users u
                        WHERE u.id = current_setting('app.current_user_id')::uuid
                        AND u.role IN('admin', 'manager')
                    )
                )
            );
        ELSE
            RAISE NOTICE 'Policy "availabilities_mod_policy" already exists. Skipping.';
        END IF;
    END $$; 
    """
    )

    availabilities_del_policy = text(
        """
DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'availabilities_del_policy') 
        THEN
            CREATE POLICY availabilities_del_policy ON availabilities
            FOR delete
            USING (
                user_id = current_setting('app.current_user_id')::uuid 
                OR 
                (
                    EXISTS (
                        SELECT 1 FROM users u
                        WHERE u.id = current_setting('app.current_user_id')::uuid
                        AND u.role IN('admin', 'manager')
                    )
                )
            );
        ELSE
            RAISE NOTICE 'Policy "availabilities_del_policy" already exists. Skipping.';
        END IF;
    END $$;
    """
    )

    # Enable row-level security on the availabilities table
    enable_rls_on_availabilities = text(
        """
    ALTER TABLE availabilities ENABLE ROW LEVEL SECURITY;
    """
    )

    conn.execute(enable_rls_on_availabilities)
    conn.execute(availabilities_sel_policy)
    conn.execute(availabilities_ins_policy)
    conn.execute(availabilities_mod_policy)
    conn.execute(availabilities_del_policy)


# Obtain a connection from the engine
# with admin_engine.connect() as conn:
#     # Execute DDL statements
#     create_default_user(conn)
#     create_function_current_organization_id(conn)
#     create_availability_security_policies(conn)
#     conn.commit()
