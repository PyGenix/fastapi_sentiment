import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 프로젝트 루트의 .env를 읽습니다.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(".env의 DATABASE_URL을 설정해 주세요.")

# PostgreSQL용 DB 엔진을 만듭니다.
# SQLite 전용 check_same_thread 옵션은 제거합니다.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 기존 04·06 lab과 같은 세션 설정을 유지합니다.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

# FastAPI 라우터가 Depends(get_db)로 DB 세션을 받습니다.
def get_db():
    with SessionLocal() as db:
        yield db
