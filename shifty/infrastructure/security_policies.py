from sqlmodel import text


# Policy function for filtering rows based on organization membership
availability_policies = text(
    """
    ALTER TABLE public.availabilities ENABLE ROW LEVEL SECURITY;

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
            OR (organization_id = current_organization_id() and current_user_is_manager())
        );
    ELSE
        RAISE NOTICE 'Policy "availabilities_ins_policy" already exists. Skipping.';
    END IF;
END $$;

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
            OR (organization_id = current_organization_id() and current_user_is_manager())
        );
    ELSE
        RAISE NOTICE 'Policy "availabilities_mod_policy" already exists. Skipping.';
    END IF;
END $$;

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
            OR (organization_id = current_organization_id() and current_user_is_manager())
        );
    ELSE
        RAISE NOTICE 'Policy "availabilities_del_policy" already exists. Skipping.';
    END IF;
END $$;
"""
)

# Policy function for filtering rows based on organization membership
users_policy = text(
    """
    ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

    -- Drop existing policy if it exists to fix circular dependency issue
    DROP POLICY IF EXISTS users_sel_policy ON users;
    
    -- Create new policy without circular dependency
    CREATE POLICY users_sel_policy ON users
    FOR SELECT  
    USING (
        -- Allow user to see their own record
        id = current_setting('app.current_user_id')::uuid
        -- For now, allow all organization users to see each other
        -- TODO: Implement proper organization filtering without circular dependency
        OR true
    );

    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'users_ins_policy')
        THEN
            CREATE POLICY users_ins_policy ON users
            FOR insert
            with check (
                true
            );
        ELSE
            RAISE NOTICE 'Policy "users_ins_policy" already exists. Skipping.';
        END IF;
    END $$;

    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'users_mod_policy')
        THEN
            CREATE POLICY users_mod_policy ON users
            FOR update
            with check (
                true
            );
        ELSE
            RAISE NOTICE 'Policy "users_mod_policy" already exists. Skipping.';
        END IF;
    END $$;
""")

commented_out = """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'users_ins_policy')
        THEN
            CREATE POLICY users_ins_policy ON users
            FOR insert
            with check (
                organization_id = current_organization_id()
                OR (organization_id = current_organization_id() and current_user_is_manager())
            );
        ELSE
            RAISE NOTICE 'Policy "users_ins_policy" already exists. Skipping.';
        END IF;
    END $$;

    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_policies
            WHERE  policyname = 'users_mod_policy')
        THEN
            CREATE POLICY users_mod_policy ON users
            FOR update
            with check (
                organization_id = current_organization_id()
                OR (organization_id = current_organization_id() and current_user_is_manager())
            );
        ELSE
            RAISE NOTICE 'Policy "users_mod_policy" already exists. Skipping.';
        END IF;
    END $$;
"""


# Policy function for filtering rows based on organization membership
shift_slots_policies = text(
    """
        ALTER TABLE public.shift_slots ENABLE ROW LEVEL SECURITY;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'shift_slots_sel_policy')
            THEN
                CREATE POLICY shift_slots_sel_policy ON shift_slots
                FOR SELECT
                USING (is_active = True and organization_id = current_organization_id());
            ELSE
                RAISE NOTICE 'Policy "shift_slots_sel_policy" already exists. Skipping.';
            END IF;
        END $$;
    """
)

# Policy function for filtering rows based on organization membership
shift_security_policies = text(
    """
        ALTER TABLE public.shifts ENABLE ROW LEVEL SECURITY;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'shifts_sel_policy')
            THEN
                CREATE POLICY shifts_sel_policy ON shifts
                FOR SELECT
                USING (organization_id = current_organization_id());
            ELSE
                RAISE NOTICE 'Policy "shifts_sel_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'shifts_ins_policy')
            THEN
                CREATE POLICY shifts_ins_policy ON shifts
                FOR insert
                with check (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "shifts_ins_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'shifts_mod_policy')
            THEN
                CREATE POLICY shifts_mod_policy ON shifts
                FOR update
                with check (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "shifts_mod_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'shifts_del_policy')
            THEN
                CREATE POLICY shifts_del_policy ON shifts
                FOR delete
                USING (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "shifts_del_policy" already exists. Skipping.';
            END IF;
        END $$
    ;
    """
)

# Policy function for filtering rows based on organization membership
overrides_security_policies = text(
    """
        ALTER TABLE public.overrides ENABLE ROW LEVEL SECURITY;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'overrides_sel_policy')
            THEN
                CREATE POLICY overrides_sel_policy ON overrides
                FOR SELECT
                USING (organization_id = current_organization_id());
            ELSE
                RAISE NOTICE 'Policy "overrides_sel_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'overrides_ins_policy')
            THEN
                CREATE POLICY overrides_ins_policy ON overrides
                FOR insert
                with check (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "overrides_ins_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'overrides_mod_policy')
            THEN
                CREATE POLICY overrides_mod_policy ON overrides
                FOR update
                with check (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "overrides_mod_policy" already exists. Skipping.';
            END IF;
        END $$;

        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_policies
                WHERE  policyname = 'overrides_del_policy')
            THEN
                CREATE POLICY overrides_del_policy ON overrides
                FOR delete
                USING (
                    user_id = current_setting('app.current_user_id')::uuid
                    OR (organization_id = current_organization_id() and current_user_is_manager())
                );
            ELSE
                RAISE NOTICE 'Policy "overrides_del_policy" already exists. Skipping.';
            END IF;
        END $$
    ;
    """
)

all_policies = [
    availability_policies,
    users_policy,
    shift_slots_policies,
    shift_security_policies,
    overrides_security_policies
]
