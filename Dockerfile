# 사용할 Python 이미지 지정
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 라이브러리를 requirements.txt로부터 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 작업 디렉토리로 복사
COPY . .

# 환경변수 설정
ENV DISCORD_BOT_TOKEN=your_token_here

# 봇 실행
CMD ["python", "app.py"]
