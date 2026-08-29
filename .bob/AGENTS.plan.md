# Plan Mode — Galaxium Travels

> Inherits all context from `../AGENTS.md`. This file adds architectural guidance for planning and design tasks.

## Architecture Summary

```
┌─────────────────────────────────┐
│  React SPA (Vite + TypeScript)  │  :5173
│  src/services/api.ts (Axios)    │
└────────────┬────────────────────┘
             │ HTTP REST
┌────────────▼────────────────────┐
│  FastAPI app  :8080             │
│  ├── REST routes (/flights, …)  │
│  └── MCP mount (/mcp)          │
│       ├── FastMCP tools         │
│       └── Shared service layer  │
├─────────────────────────────────┤
│  Service layer (services/)      │
│  booking.py / flight.py /       │
│  user.py                        │
├─────────────────────────────────┤
│  SQLAlchemy ORM → SQLite        │
│  models.py: User, Flight,       │
│             Booking             │
└─────────────────────────────────┘
```

## Design Principles
- **Dual-protocol parity**: every user-facing action is available via both REST and MCP. When adding new features, plan for both surfaces.
- **Service layer is the source of truth**: all business logic and validation lives in `services/`. REST handlers and MCP tools are thin wrappers.
- **Error model**: operations return a discriminated union (`SuccessOut | ErrorResponse`) rather than raising HTTP exceptions. Plan responses accordingly.
- **SQLite for demos**: the database is file-based and re-seeded on startup. No migrations — `init_db()` runs `create_all` on each start.

## Boundaries & Constraints
- Adding authentication is out of scope; user identification is name + email only.
- No background jobs, websockets, or push notifications; the frontend polls/re-fetches.
- Framer Motion is already in the frontend; avoid adding competing animation libraries.
- No ORM migrations are set up — schema changes require drop-and-recreate (acceptable for demo).

## Common Planning Patterns

### New data entity
1. Add ORM model → add Pydantic schema → add service functions → wire REST + MCP → update frontend types + api.ts → add UI components.

### New page
1. Create `src/pages/NewPage.tsx` → add `<Route>` in `App.tsx` → add nav link in `Header.tsx`.

### Exposing a new MCP tool
1. Implement in services → add `@mcp.tool()` decorated function in `server.py` before `mcp_app = mcp.http_app()`.
