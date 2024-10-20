class FolderTree:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.tree = {}

    def create_folder_tree(self, path):
        # フォルダツリーの作成
        parts = self.split_path(path)
        current = self.tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def split_path(self, path):
        # パスの分割
        return path.strip('/').split('/')

