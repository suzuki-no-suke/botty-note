# langserv.py

from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
import asyncio

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Celeryの設定
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# チャットリストを取得するエンドポイント
@app.get("/chatlist")
async def get_chat_list():
    # チャットリストの取得処理
    return {"chat_list": ["chat1", "chat2", "chat3"]}

# WebSocketエンドポイント
@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Celeryタスクを呼び出してバックグラウンドで処理
        await process_chat(data, websocket)

@celery_app.task
def process_chat(message, websocket):
    # メッセージ処理のロジック
    # ここでメッ���ージを処理し、必要に応じてクライアントに送信
    asyncio.run(websocket.send_text(f"Received: {message}"))

