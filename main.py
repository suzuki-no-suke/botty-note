import tornado.ioloop
import tornado.web
import os

from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------


from src.md.MarkdownRenderer import MarkdownRenderer
from src.etc.FolderParser import FolderParser, ContentType


# ---------------------------------------------------------

class EditPageHandler(tornado.web.RequestHandler):
    def get(self, path):
        savedir_base = os.getenv('FILES_ROOT', './filekeep/fileroot/')
        expected_fullpath = os.path.join(savedir_base, path)
        if os.path.exists(expected_fullpath):
            print("file exists")
            self.render("edit.html")
        else:
            print("create new file")
            self.render("edit.html")

    def post(self):
        pass

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
                                 "filekeep/fileroot/")))
        keeppath = os.getenv("KEEP_ROOT",
                            os.path.abspath(os.path.join(
                                os.path.dirname(__file__),
                                "filekeep/keep/")))
        leftmenu = renderer.render(os.path.join(keeppath, "leftmenu.md"))
        entry_path = os.path.join(basepath, path)
        if path == "":
            # root dir access
            folders = FolderParser(basepath).parse()
            title = os.path.basename(path)
            self.render("folders.html", title=title, leftmenu=leftmenu, folders=folders)
            return
        elif os.path.isfile(entry_path):
            # file access
            contents = renderer.render(entry_path)
            title = os.path.basename(path)
            self.render("view.html", title=title, leftmenu=leftmenu, contents=contents)
            return
        elif os.path.isdir(entry_path):
            # directory access
            folders = FolderParser(entry_path).parse()
            title = os.path.basename(path)
            self.render("folders.html", title=title, leftmenu=leftmenu, folders=folders)
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
        self.render("view.html", title=title, leftmenu=leftmenu, contents=indexpage)

# ---------------------------------------------------------

def make_app():
    return tornado.web.Application(
        [
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
