import os

from enum import Enum

class ContentType(Enum):
    Folder = 'folder'
    File = 'file'

class FolderParser:
    def __init__(self, base_dir, ignore=['.gitignore', '.gitkeep']):
        self.base_dir = os.path.abspath(base_dir)
        self.ignore = ignore
        #print(f"ignore config -> {self.ignore}")

    def parse(self, depth=3):
        """
        load directory from dir root and output dictionary

        Output
        ------
        {
            'name': 'basedir',
            'type': ContentType.Folder,
            'children': 10,
            'folder': [
                {
                    'name': 'somefile.md',
                    'type': ContentType.File
                    'children' : 0,
                    'folder' : [],          # need empty list when it is file
                },
                {
                    'name': 'somedir',
                    'type': ContentType.File,
                    'children': 2,          # number of file and dir (both)
                    'folder' : [
                        {
                            'name': 'otherfile.md',
                            'type': ContentType.File,
                            'children': 0,
                            'folder': [],
                        },
                        {
                            'name': 'otherdir', # depth count start as root = 1
                            'type': ContentType.File,
                            'children': 10, # actual number of file and dir 
                            'folder': [],   # most deepest folder has no items
                        },
                    ],
                }
            ]
        }

        """
        return self.parse_from(self.base_dir, depth)

    def parse_from(self, start_dir, depth=3):
        """
        load directory from specified dir and output dictionary

        Output
            - see : parse
        """
        # TODO : sort
        # TODO : adopt ignore
        result = {'name': os.path.basename(start_dir), 'type': ContentType.Folder, 'children': 0, 'folder': [], 'depth': depth}
        for entry in self.sorted_ignored_listdir(start_dir):
            result['children'] += 1
            full_path = os.path.join(start_dir, entry)
            if os.path.isdir(full_path):
                if depth <= 2:
                    children_count = len(self.sorted_ignored_listdir(full_path))
                    result['folder'].append({'name': entry, 'type': ContentType.Folder, 'children': children_count, 'folder': [], 'depth': depth - 1})
                else:
                    child_result = self.parse_from(full_path, depth - 1)
                    result['folder'].append(child_result)
            else:
                result['folder'].append({'name': entry, 'type': ContentType.File, 'children': 0, 'folder': [], 'depth': depth - 1})
        return result

    def sorted_ignored_listdir(self, dirpath):
        """
        sort (dir を先に、file を後に、いずれも辞書順で)
        そして ignore を除去したファイル・フォルダをリストで返す
        """
        dirs = []
        files = []
        alphabetic_ignored = sorted(filter(lambda x: x not in self.ignore,
                                            os.listdir(dirpath)),
                                    key=lambda x: x.lower())
        for entry in alphabetic_ignored:
            full_path = os.path.join(dirpath, entry)
            if os.path.isdir(full_path):
                dirs.append(entry)
            else:
                files.append(entry)
        return dirs + files
