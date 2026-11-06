# FastAPI Sentiment

Python FastAPI app for Hugging Face sentiment analysis with optional SQLAlchemy CRUD, Redis cache, and Celery async workers.

## Stack

- **Backend:** Python 3.12+, FastAPI, Uvicorn, Jinja2 templates
- **ML:** Hugging Face Transformers (CPU PyTorch)
- **DB:** SQLite + SQLAlchemy
- **Async:** Redis + Celery (optional via Docker Compose)

## Features

- Synchronous `/predict/` analysis page and API
- CRUD for saved text items with re-analysis
- Async create/update path via Celery worker
- Redis cache for repeated inferences
- Pytest coverage for health, CRUD, and predict flows

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- Predict UI: http://127.0.0.1:8000/predict/
- Health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

Optional async stack:

```bash
docker compose up -d
celery -A sentiment.celery_app:celery_app worker --loglevel=info --pool=solo
python -m sentiment.migrate_06
uvicorn main:app --reload
```

## Author

Pooja Sharma — [Pooja101117](https://github.com/Pooja101117)
