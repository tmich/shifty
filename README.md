# Shifty 🕒

A modern shift scheduling API with availability management, override handling, and flexible shift fragmentation.  
Built with FastAPI, SQLModel, and tested with Pytest.

---

## 🔧 Features

- 📆 Create and manage **availability** and **shifts**
- 🧠 **Automatic shift generation** based on user availability and rules
- 🧑‍🤝‍🧑 Assign shifts to users
- 🔁 Request and fulfill **shift overrides** (including partial ones)
- 🧩 Automatic **fragmentation** of shifts on partial override fulfillment
- 🔒 JWT authentication (via Supabase)
- ✅ Full test coverage with Pytest

---

## 🧱 Architecture Overview

Shifty follows Clean Architecture principles:

- **Domain layer** – Core entities and business logic (e.g. `Shift`, `Override`)
- **Application layer** – Use cases and DTOs
- **Infrastructure layer** – Database models (SQLModel), auth
- **API layer** – FastAPI routes and dependency wiring

---

## 📐 Example: Partial Override Flow

1. Mario has a shift from `10:00 → 18:00`
2. He creates an override request for `12:00 → 16:00`
3. Giovanni accepts to cover only `13:00 → 14:00`
4. System splits the original shift into 5:

    - `10:00–12:00` – Mario
    - `12:00–13:00` – Mario (unclaimed override)
    - `13:00–14:00` – Giovanni (claimed override)
    - `14:00–16:00` – Mario (unclaimed override)
    - `16:00–18:00` – Mario

All fragments track their parent (`parent_shift_id`) and carry override status.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
poetry install
# or
pip install -r requirements.txt
```

### 2. Run the API

```bash
uvicorn shifty.main:app --reload
```

### 3. Run tests

```bash
pytest
```

## 📂 Project Structure

```bash
shifty/
├── api/                # FastAPI routes
├── domain/             # Entities, enums, rules
├── application/        # Use cases, DTOs
├── infrastructure/     # SQLModel models, DB logic
├── tests/              # Pytest suite
└── main.py             # App entrypoint
```

## ✨ Roadmap

- WebSocket updates for live shift changes
- Notification system for override requests
- Role-based access control
- Shifty Client SDK (TypeScript)

## 🛡 License

MIT License

## 🤝 Contributing

Fork, PR, or open issues! All contributions are welcome.

##  🔗 Related Projects

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
