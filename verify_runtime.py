"""Verify runtime completion without a fake model and save the result."""
import json
from pathlib import Path
from fastapi.testclient import TestClient
from main import app
from sentiment.hf_model import get_classifier, normalize_prediction


def main():
    text = "오늘 정말 기분이 좋아요"
    result = normalize_prediction(get_classifier()(text, truncation=True, max_length=512))
    with TestClient(app) as client:
        checks = {
            "health": client.get("/health").status_code,
            "predict_get": client.get("/predict/").status_code,
            "empty_post": client.post("/predict/", data={"text": " "}).status_code,
            "long_post": client.post("/predict/", data={"text": "가" * 501}).status_code,
            "css": client.get("/static/css/sentiment.css").status_code,
            "docs": client.get("/docs").status_code,
        }
        response = client.post("/predict/", data={"text": text})
        checks["real_predict_post"] = response.status_code
        expected = {"health": 200, "predict_get": 200, "empty_post": 400, "long_post": 400, "css": 200, "docs": 200, "real_predict_post": 200}
        if checks != expected or result["label"] not in response.text:
            raise RuntimeError(f"실행 검증 실패: {checks}")
    report = {"checks": checks, "model_result": {"input": text, **result}}
    output = Path(".setup/runtime_check.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Real model and runtime checks passed")


if __name__ == "__main__":
    main()
