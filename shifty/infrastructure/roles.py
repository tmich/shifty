import os
from sqlmodel import text

create_default_role = text(f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_roles
            WHERE  rolname = '{os.getenv('SHIFTY_USER', 'shifty_user')}') 
        THEN
            CREATE ROLE {os.getenv('SHIFTY_USER', 'shifty_user')} LOGIN PASSWORD '{os.getenv('SHIFTY_PASSWORD', 'pwd')}';
        ELSE
            RAISE NOTICE 'Role "{os.getenv('SHIFTY_USER', 'shifty_user')}" already exists. Skipping.';
        END IF;
    END $$;

    GRANT CONNECT ON DATABASE shiftydb TO {os.getenv('SHIFTY_USER', 'shifty_user')};
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {os.getenv('SHIFTY_USER', 'shifty_user')};
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {os.getenv('SHIFTY_USER', 'shifty_user')};
    """)

all_roles = [
    create_default_role,
]