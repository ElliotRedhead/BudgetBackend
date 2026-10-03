![Django CI](https://github.com/ElliotRedhead/BudgetBackend/actions/workflows/django.yml/badge.svg)
[![codecov](https://codecov.io/gh/elliotredhead/BudgetBackend/branch/main/graph/badge.svg)](https://codecov.io/gh/elliotredhead/BudgetBackend)

# BudgetBackend

The REST API behind **Budget**, a personal budgeting app: log what you spend, set a monthly budget, and see where the money goes. Built with Django 5.2 LTS and Django REST Framework on Python 3.14.

The React frontend lives in [BudgetFrontend](https://github.com/ElliotRedhead/BudgetFrontend).

## What it does

- **Accounts:** register and log in with an email address. JWT access and refresh tokens, where refresh tokens rotate and are revoked on use and on logout.
- **Expenses:** create, edit and delete expenses with a category, cost and date. List them by month, search by name, and filter by category or cost.
- **Monthly budgets:** one budget per month. A month without its own budget uses the most recent earlier one.
- **Summary:** each month's total spend, budget and what's left, split by category.
- **Recurring expenses:** monthly bills (rent, subscriptions) added to a month in one step. Applying twice for the same month adds nothing new.
- **CSV import and export:** in the same format both ways. An import is all-or-nothing, with errors reported by row.
- **OpenAPI schema:** Swagger UI at `/schema/swagger`, and a committed `schema.yml` that CI keeps up to date.

## Architecture

```mermaid
flowchart LR
    browser["BudgetFrontend<br/>React + Vite"] -- "JSON over HTTPS<br/>JWT in the Authorization header" --> views
    subgraph api["BudgetBackend"]
        direction TB
        views["DRF viewsets<br/>(scoped to the requesting user)"] --> models["Django models<br/>User · Expense · Budget · RecurringExpense"]
    end
    models --> db[("PostgreSQL 18")]
    cron["Monthly job<br/>apply_recurring_expenses"] -.-> models
```

## Getting started

### Everything in Docker (recommended)

Clone both repositories side by side, then start the database, API and frontend together:

```sh
git clone https://github.com/ElliotRedhead/BudgetBackend.git
git clone https://github.com/ElliotRedhead/BudgetFrontend.git
cd BudgetBackend
docker compose up --build
```

- Frontend: http://localhost:3000. Log in as `demo@example.com` / `demo-budget-2026`. The demo account is reset with three months of data on every start.
- API: http://localhost:8000, with docs at http://localhost:8000/schema/swagger.

If port 3000 is taken, run `FRONTEND_PORT=3001 docker compose up` instead.

### API only, without Docker

Requires [uv](https://docs.astral.sh/uv/). It installs Python 3.14 if you don't have it.

```sh
uv sync
cp .env.template .env   # then set DJANGO_SECRET_KEY
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

Leaving `DATABASE_URL` unset uses SQLite.

## API overview

| Endpoint | Methods | Purpose |
|---|---|---|
| `/user/register/` | POST | Create an account; returns the email and a JWT pair |
| `/user/login/` | POST | Exchange email and password for a JWT pair |
| `/user/refresh/` | POST | Exchange a refresh token for a new pair (the old one is revoked) |
| `/user/logout/` | POST | Revoke a refresh token |
| `/expenses/` | GET, POST | List (paginated, filterable) or create expenses |
| `/expenses/{id}/` | GET, PATCH, PUT, DELETE | One expense |
| `/expenses/summary/?month=YYYY-MM` | GET | Month total, budget, remaining and per-category totals |
| `/expenses/export/` | GET | CSV of the (filtered) expenses |
| `/expenses/import/` | POST | Create expenses from a CSV upload |
| `/budgets/` | GET, POST | Monthly budgets, filterable by `month` |
| `/budgets/{id}/` | GET, PATCH, PUT, DELETE | One budget |
| `/recurring-expenses/` | GET, POST | Recurring expense templates |
| `/recurring-expenses/{id}/` | GET, PATCH, PUT, DELETE | One template |
| `/recurring-expenses/apply/?month=YYYY-MM` | POST | Add the month's recurring expenses |

Authenticated requests send `Authorization: JWT <access token>`. Lists are paginated: 20 per page by default, up to 100 with `page_size`. Expense lists accept `month`, `category`, `name__icontains`, `cost__lt`, `cost__gt` and `date_range`.

## Design decisions

- **Money is stored as whole pence** (integers), never floats, so totals are exact. The API speaks pence; CSV files use pounds, for spreadsheets.
- **Every query is scoped to the requesting user** in each viewset's `get_queryset`, so detail, update and delete can't reach another user's data. Admins use the Django admin, not the API.
- **Emails are the username and case-insensitive.** They're stored lowercased and looked up with `iexact`, so Django's standard `ModelBackend` handles login.
- **Refresh tokens are single use.** simplejwt's blacklist revokes each one when it's rotated or on logout, which limits the damage from a leaked token.
- **Budgets carry forward.** The summary uses the latest budget on or before the month, so it only needs setting when it changes.
- **Recurring expenses are applied, not generated on read.** Each created expense links back to its template, which makes applying idempotent and safe to run from a button or a scheduler.

## Development

```sh
uv run pytest                     # tests (random order)
uv run ruff check . && uv run ruff format --check .
uv run mypy .                     # with the Django and DRF plugins
uv run python manage.py spectacular --file schema.yml   # after API changes
```

CI runs all of these against PostgreSQL 18 on every push and pull request. Pre-commit hooks (`uv run pre-commit install`) run ruff on each commit.

### Scheduled jobs

In production, run these on a schedule:

- `python manage.py apply_recurring_expenses`: monthly, to add everyone's recurring expenses (`--month YYYY-MM` for a specific month).
- `python manage.py flushexpiredtokens`: daily or weekly, to remove expired entries from the token blacklist.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | _(required)_ | Signing key for sessions and JWTs |
| `DJANGO_DEBUG` | `0` | `1` for local development only |
| `DATABASE_URL` | SQLite file | e.g. `postgres://user:password@host:5432/budget` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names |
| `DJANGO_CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated frontend origins |
| `DJANGO_HTTPS` | `0` | `1` behind HTTPS: secure cookies, HSTS, redirect to HTTPS |

## License

[GPL-3.0](LICENSE)
