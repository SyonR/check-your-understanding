# Agent Mode — Galaxium Travels

> Inherits all context from `../AGENTS.md`. This file adds implementation guidance specific to code editing tasks.

## Key Files to Know Before Editing

### Backend
- **`booking_system_backend/server.py`** — The only file that wires REST routes and MCP tools. Each REST endpoint calls a service function directly; each MCP tool opens its own `SessionLocal` (not the DI `get_db`).
- **`booking_system_backend/services/`** — All business logic lives here. Keep services pure: they accept a `Session` and return a Pydantic model or `ErrorResponse`. Never add HTTP concerns here.
- **`booking_system_backend/models.py`** — SQLAlchemy ORM. `User`, `Flight`, `Booking`. `booking_time` is stored as ISO 8601 string.
- **`booking_system_backend/schemas.py`** — Pydantic v2 schemas. Use `model_validate()` (not `from_orm()`).

### Frontend
- **`booking_system_frontend/src/services/api.ts`** — Single Axios instance. All API calls go through this. Base URL from `VITE_API_URL` env var (default `http://localhost:8080`).
- **`booking_system_frontend/src/types/index.ts`** — Shared TypeScript types that mirror backend schemas.
- **`booking_system_frontend/src/hooks/useUser.tsx`** — `UserContext` and `UserProvider`. Access the logged-in user with `useUser()`.
- **`booking_system_frontend/src/App.tsx`** — Route definitions. Add new pages here.

## Conventions

### Python (Backend)
- Services return `ModelOut | ErrorResponse` — never raise HTTP exceptions from the service layer.
- Error responses always include `error`, `error_code`, and a descriptive `details` string.
- Use `db.query(Model).filter(...).first()` pattern.
- Run `pytest` from `booking_system_backend/` to validate.

### TypeScript (Frontend)
- Functional components with hooks only — no class components.
- Use `isErrorResponse()` helper from `api.ts` to discriminate error vs success responses.
- Tailwind utility classes for all styling; custom colours in `tailwind.config.js`.
- Run `npm run lint` from `booking_system_frontend/` to validate.

## Adding a New Feature (checklist)
1. Add/update SQLAlchemy model in `models.py` if schema change needed.
2. Add/update Pydantic schema in `schemas.py`.
3. Implement business logic in the appropriate `services/*.py` file.
4. Expose via REST in `server.py` (`@app.get/post`).
5. Expose via MCP in `server.py` (`@mcp.tool()`).
6. Add/update the Axios function in `api.ts`.
7. Update TypeScript types in `types/index.ts`.
8. Build or update the React component/page.
9. Run `pytest` + `npm run lint` to confirm green.
