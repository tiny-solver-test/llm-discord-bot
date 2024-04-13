import logging

def get_logger(name):
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 로그 레벨 설정

    # 로그 포맷 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 스트림 핸들러 생성 및 추가
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(stream_handler)

    return logger
