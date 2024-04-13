import discord
from discord import Message
import os
from llm import query_local_api, create_thread_title

# load dotenv from .env file
from dotenv import load_dotenv
load_dotenv()

from config import get_logger

logger = get_logger(__name__)

DISCORD_BOT_TOKEN=os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 읽기 위한 권한 활성화
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')  # 로그인 확인 메시지 출력

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return  # 봇 자신의 메시지는 처리하지 않음

    # '!llm'으로 시작하는 메시지 처리
    if message.content.startswith('!llm'):
        question = message.content[len('!llm '):]  # 명령어를 제외한 질문 부분 추출
        if question:  # 질문이 있을 때만 처리
            logger.info(f"question...")
            response = query_local_api(question)  # 로컬 API에 질문 요청
            logger.info(f"answer...")
            thread_title = create_thread_title(question, response)  # 스레드 제목을 위한 추가 요청
            logger.info(f"generate title...")

            # 스레드에서 메시지가 온 경우
            if message.channel.type == discord.ChannelType.public_thread:
                logger.info(f"Received message in thread: {message.channel.name}")
                await message.channel.send(response)  # 스레드에 응답
            else:
                # 스레드 생성 및 응답
                logger.info(f"Creating thread: {thread_title}")
                new_thread = await message.create_thread(name=thread_title, reason="Auto-created thread for LLM query")
                logger.info(f"Sending response to thread: {thread_title}")
                await new_thread.send(response)
        else:
            await message.channel.send("질문을 입력해주세요.")  # 질문이 없을 경우 안내 메시지

client.run(DISCORD_BOT_TOKEN)  # 'YOUR_BOT_TOKEN'을 실제 봇 토큰으로 교체
