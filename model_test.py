"""Download and smoke-test the real Hugging Face sentiment model."""
from sentiment.hf_model import get_classifier, normalize_prediction

if __name__ == "__main__":
    text = "오늘 정말 기분이 좋아요"
    result = normalize_prediction(get_classifier()(text, truncation=True, max_length=512))
    print({"input": text, **result})
