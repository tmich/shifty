-- Utente
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'supervisor', 'worker')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Attività (es. bar, ristorante)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    timezone TEXT DEFAULT 'Europe/Rome'
);

-- Collegamento utente ↔ attività
CREATE TABLE user_organization (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, organization_id)
);

-- Disponibilità settimanale (es. lunedì: 08:00–12:00)
CREATE TABLE availabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Slot definiti dall'attività (es. Mattina 8-12)
CREATE TABLE shift_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name TEXT,
    start_time TIME,
    end_time TIME
);

-- Turno specifico
CREATE TABLE shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES shift_templates(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    date DATE NOT NULL,
    override_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Assegnazione turni
CREATE TABLE shift_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    shift_id UUID REFERENCES shifts(id),
    user_id UUID REFERENCES users(id),
    partial_start TIME,
    partial_end TIME,
    note TEXT
);

-- Timesheet (presenze effettive)
CREATE TABLE timesheets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    shift_id UUID REFERENCES shifts(id),
    check_in TIMESTAMP,
    check_out TIMESTAMP,
    approved BOOLEAN DEFAULT FALSE
);


-- DML

INSERT INTO public.users (id,email,full_name,role,created_at,is_active) VALUES
	 ('e9f237b6-fbc4-4ff8-933d-26d022c68339'::uuid,'prova@shifty.com','Prova Provona','worker','2025-06-14 17:14:21.090007', true);

INSERT INTO public.organizations (id,name,description,created_at) VALUES
	 ('a8561caf-c324-4bdd-af4b-15e8a15f2c40'::uuid,'Shifty App','A simple organization',localtimestamp);

INSERT INTO public.user_organizations (user_id,organization_id) VALUES
	 ('e9f237b6-fbc4-4ff8-933d-26d022c68339'::uuid,'a8561caf-c324-4bdd-af4b-15e8a15f2c40'::uuid);   
