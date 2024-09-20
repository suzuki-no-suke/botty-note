import marko
import os

class MarkdownRenderer:
    def render(self, file):
        # open file
        if not os.path.isfile(file):
            raise FileNotFoundError()
        with open(file, "rt", encoding="utf-8") as f:
            content = f.read()

        # render
        content = marko.convert(content)

        # TODO : some adaptational process

        return content
