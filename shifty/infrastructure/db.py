from typing import Generator
from sqlmodel import Session, create_engine, text

# create a new postgresql database
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5431/shiftydb", echo=True, future=True)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dipendenza FastAPI
def get_session() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# roles and permissions
# with engine.connect() as connection:
#     query = """
#     CREATE USER IF NOT EXISTS shifty_user WITH PASSWORD 'shifty_password'
#     GRANT CONNECT ON DATABASE shiftydb TO shifty_user;
#     GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO shifty_user;
#     GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO shifty_user;
#     """
#     connection.execute(text(query))
#     connection.commit()

def define_security_policies(engine):
    # Policy function for filtering rows based on user_id
    policy_function = text(
    """
    CREATE OR REPLACE POLICY availability_select_policy ON availabilities
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1
            FROM users
            INNER JOIN organizations ON users.organization_id = organizations.id
            INNER JOIN availabilities ON users.id = availabilities.user_id
            WHERE users.organization_id = availabilities.organization_id
            AND users.id = current_setting('app.current_user_id')::uuid
        )
    );
    """
    )

    # Set the default row-level security policy
    default_policy = text(
    """
    ALTER TABLE availabilities ENABLE ROW LEVEL SECURITY;
    """
    )

    # Obtain a connection from the engine
    with engine.connect() as conn:
        # Execute DDL statements
        conn.execute(policy_function)
        conn.execute(default_policy)
        conn.commit()


# define_security_policies(engine)
