import tornado
import tornado.web

from dotenv import load_dotenv
load_dotenv()

import os

from src.orm.Base import SQLFactory


# ---------------------------------------------------------

class ListChatbotHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class ChatOpeningHandler(tornado.web.RequestHandler):
    def get(self, history_id):
        dbobj = SQLFactory.default_env()

        # access db 
        pass



class WebSocketCallbacks:
    def on_open(self, ws_future):
        pass

    def on_message(self):
        pass

    def on_close(self):
        pass

class ChatMessageRequest(tornado.web.RequestHandler):
    def post(self):
        # validating post

        # access db and find history_id

        # accessing relay server with WebSocket client

        # calling LLM agent
        # and its callback

        # finish LLM calling

        # close WebSocket client

        pass



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
