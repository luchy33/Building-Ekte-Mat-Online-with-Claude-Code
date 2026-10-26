# Ekte Mat Online

Ordering system for Ekte Mat AS, a fictional catering company in Bergen. It replaces orders by e-mail, phone and Excel. Built with Flask (MVC) for INFO212 Oblig 4. All data is synthetic.

- **Shop**: menu by event type (cart, orders and questions come in later plans)
- **Account**: customer pages (placeholder)
- **Admin**: food items, images, orders and questions (placeholder)

## Getting started

Requires Python 3.10 or newer.

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then edit SECRET_KEY and SEED_PASSWORD
python seed.py              # resets the database with synthetic data
flask --app app run         # http://127.0.0.1:5000
pytest
```

**macOS / Linux / Git Bash**
```bash
python -m venv .venv
source .venv/bin/activate   # Git Bash on Windows: source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
flask --app app run
pytest
```

`flask --app app init-db` creates empty tables without seed data. The SQLite file is `instance/ektemat.sqlite`.

Seeded accounts: `admin@ektemat.example` (admin), `private.customer@example.com` and `lunch@corporate.example.com`. They all use the password set in `SEED_PASSWORD`.

## Structure

- `app/models/`: domain classes (dataclasses, no database code)
- `app/models/repositories/`: the only code that touches the database
- `app/controllers/`: blueprints `shop`, `account` and `admin`
- `app/templates/`: Jinja2 views, one folder per blueprint
- `tests/`: pytest
- `docs/plans/`: agreed feature plans, starting with [01-skeleton.md](docs/plans/01-skeleton.md)
- `labb_claude_cowork/`: Lab 7 requirements and models (read-only)

See [CLAUDE.md](CLAUDE.md) for the project rules.
