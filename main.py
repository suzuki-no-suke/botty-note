import tornado.ioloop
import tornado.web
import tornado.websocket

import os
import json

from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------


from src.md.MarkdownRenderer import MarkdownRenderer
from src.etc.FolderParser import FolderParser, ContentType


# ---------------------------------------------------------

class EditPageHandler(tornado.web.RequestHandler):
    def get(self, path):
        if path == "":
            # just create new file
            print("create new file")
            self.render("edit.html", isnew=True, title=None, path="", current_contents="")
            return

        savedir_base = os.path.abspath(os.getenv('FILES_ROOT', './filekeep/fileroot/'))
        expected_fullpath = os.path.abspath(os.path.join(savedir_base, path))
        if os.path.isfile(expected_fullpath):
            print(f"file exists : {path}")
            with open(expected_fullpath, "rt", encoding="utf-8") as f:
                content = f.read()
            self.render("edit.html", isnew=False, title=path, path=path, current_contents=content)
            return
        elif os.path.isdir(expected_fullpath):
            self.redirect(f"/view/{path}")
            return
        else:
            print(f"create new file with path -> {path}")
            self.render("edit.html", isnew=True, title=path, path=path, current_contents="")
            return

    def post(self, path):
        # get parameters
        filename = self.get_argument("filename")
        content = self.get_argument("content")
        isnew = self.get_argument("isnew")
        prev_title = self.get_argument("prev_title", "")

        print(f"filename -> {filename}")

        # validation and error
        if not filename:
            isnew_flag = isnew == "t"
            prev_title = None if prev_title == "" else prev_title
            self.render("edit.html", isnew=isnew_flag, title=prev_title, path=filename, current_contents=content)
            return

        # validation cleared
        savedir_base = os.path.abspath(os.getenv('FILES_ROOT', './filekeep/fileroot/'))
        expected_fullpath = os.path.abspath(os.path.join(savedir_base, filename))
        if os.path.exists(expected_fullpath):
            # overwrite
            with open(expected_fullpath, "wt", encoding="utf-8") as f:
                f.write(content)
            self.redirect(f"/view/{filename}")
        else:
            # create file
            # フォルダが存在しなければ作成
            os.makedirs(os.path.dirname(expected_fullpath), exist_ok=True)
            # 新規ファイルを作成
            with open(expected_fullpath, "wt", encoding="utf-8") as f:
                f.write(content)
            self.redirect(f"/view/{filename}")



class ViewPageHandler(tornado.web.RequestHandler):
    def get(self, path):
        print(f"access to {path}")

        # TODO : defence from directory traversal

        # prepare markdown renderer
        renderer = MarkdownRenderer()

        # TODO : respawn keep files

        # パスをフォルダかファイルか存在しないか判別
        basepath = os.getenv("FILES_ROOT",
                             os.path.abspath(os.path.join(
                                 os.path.dirname(__file__),
                                 "./filekeep/fileroot/")))
        keeppath = os.getenv("KEEP_ROOT",
                            os.path.abspath(os.path.join(
                                os.path.dirname(__file__),
                                "./filekeep/keep/")))
        leftmenu = renderer.render(os.path.join(keeppath, "leftmenu.md"))
        entry_path = os.path.join(basepath, path)
        print(f"debug : base -> {basepath}, keep -> {keeppath}")
        print(f"debug : entry path -> {entry_path}")
        #isfile = os.path.isfile(entry_path)
        #isdir = os.path.isdir(entry_path)
        #print(f"debug : fullpath -> {entry_path}, isfile {isfile}, isdir {isdir}")
        if path == "":
            # root dir access
            altbase = ""
            folders = FolderParser(basepath).parse()
            title = "(root)"
            self.render("folders.html", title=title, altbase=altbase, leftmenu=leftmenu, folders=folders)
            return
        elif os.path.isfile(entry_path):
            # file access
            contents = renderer.render(entry_path)
            title = os.path.basename(path)
            self.render("view.html", title=title, leftmenu=leftmenu, contents=contents, path=path)
            return
        elif os.path.isdir(entry_path):
            # directory access
            altbase = path + "/"
            folders = FolderParser(entry_path).parse()
            title = os.path.basename(path)
            self.render("folders.html", title=title, altbase=altbase, leftmenu=leftmenu, folders=folders)
            return
        else:
            # redirect to create page
            self.redirect(f"/edit/{path}")
            return
        # otherwise
        self.send_error(404)

class TopPageHandler(tornado.web.RequestHandler):
    def get(self):
        # prepare markdown renderer
        renderer = MarkdownRenderer()

        # TODO : respawn keep files

        # render indeex.md
        keeppath = os.getenv("KEEP_ROOT",
                            os.path.abspath(os.path.join(
                                os.path.dirname(__file__),
                                "filekeep/keep/")))

        leftmenu = renderer.render(os.path.join(keeppath, "leftmenu.md"))
        indexpage = renderer.render(os.path.join(keeppath, "index.md"))
        title = "Welcome to Botty Note"
        self.render("view.html", title=title, leftmenu=leftmenu, contents=indexpage, path=None)

# ---------------------------------------------------------
# LLM Server function

""" Definition Note
connections = {
    'history_id': {
        'ws': <WebSocketServer>,
        'messages': [
            {   # chat v1 definition
                'sender': <'human', 'chatbot'>,
                'message': <str>
            },
            ...
        ]
    }
}
"""
connections = {}

# LLM Relay Ready Server
class RelayOpeningHandler(tornado.web.RequestHandler):
    async def get(self, history_id):
        # get known internal endpoint
        llm_portno = os.getenv("LLM_SERV_PORTNO", 7777)
        llm_server_endpoint = f"http://localhost:{llm_portno}/chat/open/{history_id}"

        # 非同期リクエストを作成
        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(llm_server_endpoint)
            print(response)
            self.write(response.body)
        except Exception as e:
            self.set_status(500)
            self.write(f"Error: {str(e)}")

# LLM Relay Websocket server
class WebSocketRelayServer(tornado.websocket.WebSocketHandler):
    def on_open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(f"Received message: {message}")
        parsed_data = json.loads(message)
        you_said = parsed_data['message']
        response = {'type': 'chatbot', 'message': f"Echo : {you_said}"}
        self.write_message(response)

    def on_close(self):
        print("WebSocket closed")



# ---------------------------------------------------------

def make_app():
    return tornado.web.Application(
        [
            (r"/chat/open/(.*)", RelayOpeningHandler),
            (r"/chat/ws/(.*)", WebSocketRelayServer),
            (r"/edit/(.*)", EditPageHandler),
            (r"/view/(.*)", ViewPageHandler),
            (r"/", TopPageHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == "__main__":
    app = make_app()
    portno = os.getenv('PORTNO', 8888)
    app.listen(portno)
    print(f"Server is running on http://localhost:{portno}")
    tornado.ioloop.IOLoop.current().start()
