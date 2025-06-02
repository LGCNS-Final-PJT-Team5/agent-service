FROM python:3.8-slim AS builder

WORKDIR /app

# 빌드에 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치 최적화
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 소스 복사 (나중에 진행해서 캐시 최적화)
COPY . .

# 사용할 포트 명시적으로 표시
EXPOSE 60010

CMD ["python", "manage.py", "runserver", "0.0.0.0:60010"]