#!/usr/bin/env bash
set -Eeuo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p .setup
exec > >(tee -a .setup/setup.log) 2>&1
trap 'echo "설치 또는 검증이 중단됐습니다. .setup/setup.log의 마지막 오류를 확인하세요." >&2' ERR

printf '\n[1/6] uv 준비\n'
if command -v uv >/dev/null 2>&1; then
    UV_BIN="$(command -v uv)"
elif [[ -x "$PWD/.tools/bin/uv" ]]; then
    UV_BIN="$PWD/.tools/bin/uv"
elif [[ -x "$HOME/.local/bin/uv" ]]; then
    UV_BIN="$HOME/.local/bin/uv"
else
    if command -v curl >/dev/null 2>&1; then
        curl --fail --location --show-error https://astral.sh/uv/install.sh --output .setup/uv-install.sh
    elif command -v python3 >/dev/null 2>&1; then
        python3 -c 'import urllib.request; urllib.request.urlretrieve("https://astral.sh/uv/install.sh", ".setup/uv-install.sh")'
    else
        echo 'curl 또는 python3가 필요합니다.' >&2
        exit 1
    fi
    UV_INSTALL_DIR="$PWD/.tools/bin" UV_NO_MODIFY_PATH=1 sh .setup/uv-install.sh
    UV_BIN="$PWD/.tools/bin/uv"
fi
"$UV_BIN" --version

printf '\n[2/6] Python 3.12 가상환경 생성\n'
if [[ ! -x .venv/bin/python ]]; then
    "$UV_BIN" venv --python 3.12 .venv
fi
PYTHON_BIN="$PWD/.venv/bin/python"
"$PYTHON_BIN" --version

printf '\n[3/6] Install packages (first download may take a while)\n'
# GPU 드라이버 설정 없이 lab할 수 있도록 CPU용 torch를 설치합니다.
"$UV_BIN" pip install --python "$PYTHON_BIN" torch --index-url https://download.pytorch.org/whl/cpu
"$UV_BIN" pip install --python "$PYTHON_BIN" -r requirements.in
"$UV_BIN" pip freeze --python "$PYTHON_BIN" > requirements.txt

printf '\n[4/6] Run automated tests\n'
"$PYTHON_BIN" -m pytest -q

printf '\n[5/6] 실제 Hugging Face 모델 다운로드 및 웹 요청 검증\n'
"$PYTHON_BIN" verify_runtime.py

printf '\n[6/6] 서버 실행\n'
echo '브라우저: http://127.0.0.1:8000/predict/'
echo '종료: Ctrl+C / 다음 실행: bash run.sh'
exec "$PYTHON_BIN" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
