import tornado.ioloop
import tornado.web
import os

from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------

def render_leftmenu(self):
    pass

def render_toppage(self):
    pass

def render_page(self, path):
    pass




# ---------------------------------------------------------

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class EditPageHandler(tornado.web.RequestHandler):
    def get(self, path):
        savedir_base = os.getenv('FILES_ROOT', './filekeep/fileroot/')
        expected_fullpath = os.path.join(savedir_base, path)
        title = path
        if os.path.exists(expected_fullpath):
            print("file exists")
            self.render("edit.html")
        else:
            print("create new file")
            self.render("edit.html")

    def post(self):
        pass

class ViewPageHandler(tornado.web.RequestHandler):
    def is_file(self, path):
        return True

    def is_folder(self, path):
        return False

    def get(self, path):
        # path をみてフォルダかファイルか判別
        print(f"path is -> {path}")

        # フォルダの場合
        if self.is_folder(path) or path == "/folder/test/":
            folder_structure = [
                {
                    "name": "test.md",
                    'children': None,
                },
                {
                    "name": "/subfolder",
                    'children': [
                        {
                            'name': "sample.md",
                            'children': None,
                        },
                        {
                            'name': "mediator.md",
                            'children': None,
                        }
                    ],
                },
            ]
            self.render("folders.html", title=path, folder_structure=folder_structure)
        elif self.is_file(path):
            contents_html = "<h1>this is a test<h1><p>in really -> render md to html or file highlight"
            self.render("view.html", title=path, contents=contents_html)


class FolderViewPage(tornado.web.RequestHandler):
    def get_folder_structure(self, path, level=0):
        if level > 3:  # 3階層以上は表示しない
            return []
        structure = []
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    structure.append({
                        'name': entry,
                        'children': self.get_folder_structure(full_path, level + 1)
                    })
                else:
                    structure.append({'name': entry})
        except Exception as e:
            print(f"Error reading directory {path}: {e}")
        return structure

    def get(self, path):
        print(f"target path is -> {path}")
        title = "test yade"
        folder_structure = [
            {
                "name": "test.md",
                'children': None,
            },
            {
                "name": "/subfolder",
                'children': [
                    {
                        'name': "sample.md",
                        'children': None,
                    },
                    {
                        'name': "mediator.md",
                        'children': None,
                    }
                ],
            },
        ]
        self.render("folders.html", title=title, folder_structure=folder_structure)
        """
        print(f"target path is -> {path}")
        savedir_base = os.getenv('FILES_ROOT', './filekeep/fileroot/')
        print(f"base dir -> {savedir_base}")
        abs_base = os.path.abspath(savedir_base)
        print(f"base dir (abs) -> {abs_base}")
        expected_fullpath = os.path.abspath(os.path.join(abs_base, "." + path))
        print(f"fullpath is -> {expected_fullpath}")
        title = os.path.basename(expected_fullpath)
        folder_structure = self.get_folder_structure(expected_fullpath)
        self.render("folders.html", title=title, folder_structure=folder_structure)
"""


# ---------------------------------------------------------

def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/edit/(.+)", EditPageHandler),
            (r"/folder(.*)", FolderViewPage),
            (r"/view(.*)", ViewPageHandler)
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
