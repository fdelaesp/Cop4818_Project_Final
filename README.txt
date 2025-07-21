# FVD22 Macro‑Financial Indicator Explorer

A Flask web app that lets users browse Panamanian macro‑financial indicators, log in, and view simple usage analytics.

## Features
* **Authentication & sessions** (Flask‑Login)
* **SQLite → PostgreSQL** via SQLAlchemy
* **Bootstrap 5** responsive UI
* Basic **admin analytics** page
* Ready for **one‑click deployment** (Render / Fly.io)

## Quick start (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app:create_app() create-db
python import_data.py
flask --app app:create_app() run
