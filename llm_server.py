import tornado
import tornado.web
import asyncio

from dotenv import load_dotenv
import tornado.websocket
load_dotenv()

import os

import json

from src.orm.Base import SQLFactory

import time

# ---------------------------------------------------------

class ListChatbotHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('function not implemented')

class ChatOpeningHandler(tornado.web.RequestHandler):
    def get(self, history_id):
        dbobj = SQLFactory.default_env()

        # access db
        pass

        self.write(f"heart braking not implmemented : {history_id} <- ")



class WebSocketCallbacks:
    def __init__(self):
        self.ws = None

    def on_open(self, ws_future):
        self.ws = ws_future.result()
        print("connection established")

    def on_message(self, msg):
        print(f"message caught (and ignored) : {msg}")

    def on_close(self):
        self.ws = None
        print("connection closed")

    async def ensure_connected(self):
        for i in range(100):
            if self.ws is not None:
                break
            else:
                await asyncio.sleep(0.5)


    async def run_llm_async(self, message):
        await self.ensure_connected()

        # call llms
        await asyncio.sleep(5.0)
        response = {
            'type': 'chatbot',
            'message': f"echo now : {message['message']}"
        }
        self.ws.write_message(response)


class ChatMessageRequest(tornado.web.RequestHandler):
    async def post(self):
        # parse message
        print(f"body -> {self.request.body}")
        parsed_data = json.loads(self.request.body)
        ws_endpoint = parsed_data['endpoint']

        # TODO : validating post

        # TODO : access db and find history_id

        # accessing relay server with WebSocket client
        callbacks = WebSocketCallbacks()
        connection = await tornado.websocket.websocket_connect(
            ws_endpoint,
            callback=callbacks.on_open,
            on_message_callback=callbacks.on_message,
        )

        # call LLM
        await callbacks.run_llm_async(parsed_data)

        # close WebSocket client
        connection.close()


def make_app():
    return tornado.web.Application(
        [
            (r"/chatbot/", ListChatbotHandler),
            (r"/chat/open/(.*)", ChatOpeningHandler),
            (r"/chat/send/", ChatMessageRequest),
        ]
    )

if __name__ == "__main__":
    app = make_app()
    portno = os.getenv('LLM_SERV_PORTNO', 7777)
    app.listen(portno)
    print(f"LLM Server is running on http://localhost:{portno}")
    tornado.ioloop.IOLoop.current().start()
