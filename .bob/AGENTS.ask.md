# Ask Mode — Galaxium Travels

> Inherits all context from `../AGENTS.md`. This file adds reference details useful when answering questions about the project.

## Quick Reference

### Backend endpoints (no auth required)
| Method | Path | Body / Params | Returns |
|--------|------|---------------|---------|
| GET | `/` | — | `{ status: "OK" }` |
| GET | `/flights` | — | `FlightOut[]` |
| POST | `/book` | `{ user_id, name, flight_id }` | `BookingOut \| ErrorResponse` |
| GET | `/bookings/{user_id}` | — | `BookingOut[]` |
| POST | `/cancel/{booking_id}` | — | `BookingOut \| ErrorResponse` |
| POST | `/register` | `{ name, email }` | `UserOut \| ErrorResponse` |
| GET | `/user` | `?name=&email=` | `UserOut \| ErrorResponse` |

### MCP tools (at `/mcp`)
`list_flights()` · `book_flight(user_id, name, flight_id)` · `get_bookings(user_id)` · `cancel_booking(booking_id)` · `register_user(name, email)` · `get_user_id(name, email)`

### Data models
| Model | Key fields |
|-------|-----------|
| `User` | `user_id`, `name`, `email` |
| `Flight` | `flight_id`, `origin`, `destination`, `departure_time`, `arrival_time`, `price`, `seats_available` |
| `Booking` | `booking_id`, `user_id`, `flight_id`, `status` (`booked`/`cancelled`/`completed`), `booking_time` (ISO 8601) |

### Error codes
`FLIGHT_NOT_FOUND` · `NO_SEATS_AVAILABLE` · `USER_NOT_FOUND` · `NAME_MISMATCH` · `BOOKING_NOT_FOUND` · `ALREADY_CANCELLED`

### Frontend routes
| URL | Page |
|-----|------|
| `/` | Home |
| `/flights` | Flight listing and booking |
| `/bookings` | User's bookings (requires login) |

### Design tokens (Tailwind)
- `space-dark` `#030712` · `cosmic-purple` `#6366F1` · `nebula-pink` `#EC4899` · `alien-green` `#10B981` · `solar-orange` `#F59E0B`

### Demo seed data
10 users (Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Heidi, Ivan, Judy), 10 interplanetary flights, 20 sample bookings. Seeded fresh on every server start.
