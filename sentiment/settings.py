import os

# FastAPI와 Celery Worker를 모두 호스트/WSL 가상환경에서 실행합니다.
# Docker에는 Redis만 띄우므로 localhost:6380을 공통으로 사용합니다.
REDIS_CACHE_URL = os.getenv("REDIS_CACHE_URL", "redis://127.0.0.1:6380/1")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6380/2")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6380/3")
CACHE_SECONDS = 600
