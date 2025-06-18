from sqlmodel import text


# Function to get the current user ID from the session
current_user_id = text(
    """
    CREATE OR REPLACE FUNCTION public.current_user_id()
     RETURNS uuid
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN current_setting('app.current_user_id')::uuid;
    END; $function$
    ;
    """
)


# Function to get the current organization ID based on the user's organization membership
current_organization_id = text(
    """
    CREATE OR REPLACE FUNCTION public.current_organization_id()
     RETURNS uuid
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN (SELECT organization_id FROM users WHERE id = current_setting('app.current_user_id')::uuid);
    END; $function$
    ;
    """
)


# Function to get the current user's role
current_user_role = text(
    """
    CREATE OR REPLACE FUNCTION public.current_user_role()
     RETURNS text
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN (SELECT role FROM users WHERE id = current_setting('app.current_user_id')::uuid);
    END; $function$
    ;
    """
)

# Function to check if the current user is a manager
current_user_is_manager = text(
    """
    CREATE OR REPLACE FUNCTION public.current_user_is_manager()
     RETURNS boolean
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN (SELECT role = 'manager' FROM users WHERE id = current_setting('app.current_user_id')::uuid);
    END; $function$
    ;
    """
)

current_user_is_admin = text(
    """
    CREATE OR REPLACE FUNCTION public.current_user_is_admin()
     RETURNS boolean
     LANGUAGE plpgsql
     SECURITY DEFINER
    AS $function$
    BEGIN
        RETURN (SELECT role = 'admin' FROM users WHERE id = current_setting('app.current_user_id')::uuid);
    END; $function$
    ;
    """
)

all_functions = [
    current_user_id,
    current_organization_id,
    current_user_role,
    current_user_is_manager,
    current_user_is_admin,
]