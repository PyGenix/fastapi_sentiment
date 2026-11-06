from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sentiment.router import router as sentiment_router
from sentiment.db import Base, engine
from sentiment import models  # TextItem 테이블을 SQLAlchemy에 등록

app = FastAPI(title="FastAPI Sentiment CRUD · PostgreSQL")

# PostgreSQL에 아직 없는 테이블을 생성합니다.
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(sentiment_router)

@app.get("/health", name="health")
def health():
    return {"status": "ok"}
