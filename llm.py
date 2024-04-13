import requests
from config import get_logger
import os

logger = get_logger(__name__)

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL")

def query_local_api(question):
    """로컬 API에 질문을 요청하고 결과를 반환합니다."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    data = {
        "model": "EEVE-Korean-Instruct-10.8B-v1.0-Q4_K_M.gguf",
        "prompt": question,
        "stream": False
    }
    response = requests.post(url, json=data)  # POST 요청
    if response.status_code == 200:
        data = response.json()
        # log data using logger like function name and args
        text = data['response']  # API 응답에서 텍스트 추출
        # logger.info(f"query_local_api: question={question}, response={text}")
        return text
    else:
        logger.error(f"query_local_api: question={question}, status_code={response.status_code}, text={response.text}")
        return "에러가 발생했습니다: " + response.text  # 에러 메시지 반환
      
def create_thread_title(question, answer):
    """질문과 답변을 포함하여 스레드 제목을 생성합니다."""
    prompt = f"내용을 보고, 100자 내외 한줄로 핵심만 간단하게 제목으로 요약해주세요.\n질문:{question}\n답변:{answer}"
    logger.info("Generating thread title...")
    return query_local_api(prompt)
      