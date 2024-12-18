import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import uuid
import re
import shutil

# really implemented
# ---------------------------------------------------------

class FolderTreeNode(BaseModel):
    """フォルダの入れ子関係を、フォルダIDのみ表示する"""
    fullpath: str
    id: str
    folders: List['FolderTreeNode'] = []

class Folder(BaseModel):
    """単一フォルダのデータを表示する"""
    fullpath: str # root = /, root to this folder
    id: str # uuid4
    name: str
    num_files: int
    children: List[str] = []    # only children folder path

def parse_folder(dirpath, wikipath="/"):
    folders = {}
    nid = str(uuid.uuid4())
    node = FolderTreeNode(fullpath=wikipath, id=nid, folders=[])
    this_folder = Folder(
        fullpath=wikipath,
        id=nid,
        name=os.path.basename(dirpath) if wikipath != "/" else "(root)",
        num_files=0,
        children=[])

    for name in os.listdir(dirpath):
        entry_path = os.path.join(dirpath, name)
        if os.path.isdir(entry_path):
            f, n = parse_folder(entry_path, wikipath + name + "/")
            folders.update(f)
            # print(folders)
            node.folders.append(n)
            this_folder.children += [fol.fullpath for fol in f.values()]
        elif os.path.isfile(entry_path):
            this_folder.num_files += 1

    folders[nid] = this_folder

    return folders, node

class FolderTree(BaseModel):
    all_folders: Dict[str, Folder] = {}
    root_node: FolderTreeNode    # tree of IDs

# フォルダツリー取得（常にルートから）
@app.get("/tree", tags=["Tree"])
async def get_full_tree() -> FolderTree:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))

    if not os.path.isdir(basepath):
        raise HTTPException(status_code=503, detail=f"WRONG wiki dir configuration")

    # recursively get folders
    folders, tree = parse_folder(basepath)

    import pprint
    pprint.pprint(tree)

    return FolderTree(all_folders=folders, root_node=tree)

# ---------------------------------------------------------
# create folder

def valid_basename(basename: str) -> bool:
    return re.match(r'^[a-zA-Z0-9_\-\.\/\s\w＿・]+$', basename)

class FolderResult(BaseModel):
    folder_path: str
    succeed: bool
    message: str

class FolderCreate(BaseModel):
    parent: str # path
    name: str

@app.post("/folder/create", tags=["folders"])
async def create_folder(param: FolderCreate) -> FolderResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")
    fullwikipath = param.parent + param.name

    # return if folder name is empty or wrong format
    if not valid_basename(param.name):
        return FolderResult(
            folder_path=fullwikipath,
            succeed=False, 
            message="folder name is wrong format")

    # check parent exists
    parent_path = os.path.abspath(basepath + param.parent)
    print(f"create parent -> {parent_path}")
    if not os.path.isdir(parent_path):
        return FolderResult(
            folder_path=fullwikipath,
            succeed=False,
            message="parent folder not found")

    # error if already exists
    new_folder_path = os.path.join(parent_path, param.name)
    print(f"new folder path -> {new_folder_path}")
    if os.path.isdir(new_folder_path):
        return FolderResult(
            folder_path=fullwikipath,
            succeed=False,
            message="already exists")

    # check path trajectory
    if not new_folder_path.startswith(basepath):
        return FolderResult(
            folder_path=fullwikipath,
            succeed=False,
            message="path trajectory failure.")

    # create folder
    os.makedirs(new_folder_path)
    return FolderResult(folder_path=fullwikipath, succeed=True, message="Folder created successfully")


# ---------------------------------------------------------
# folder detail

class FolderDetail(BaseModel):
    """単一フォルダのデータ(詳細)を表示する"""
    fullpath: str # root = /, root to this folder
    id: str # uuid4
    name: str
    parents: List[str] = [] # parent directories (fullpath)
    files: List[str] = []   # file names (name only)
    children: List[str] = []    # only children folder path (fullpath)


@app.get("/folder/detail", tags=["folders"])
async def get_folder_detail(dirpath: str) -> FolderDetail | FolderResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))

    # check parent exists
    dir_fullpath = os.path.abspath(basepath + dirpath)
    print(f"target fullpath -> {dir_fullpath}")
    if not os.path.isdir(dir_fullpath):
        return FolderResult(
            folder_path=dirpath,
            succeed=False,
            message="folder not exists")

    # check path trajectory
    if not dir_fullpath.startswith(basepath):
        return FolderResult(
            folder_path=dirpath,
            succeed=False,
            message="path trajectory failure.")

    # gether folder information
    folder_info = FolderDetail(
        fullpath=dirpath,
        id=str(uuid.uuid4()),   # TODO : uuid fixed values
        name=os.path.basename(dirpath),
        parents=[],
        files=[],
        children=[])

    # parent path gethering
    folders = [s.strip() for s in dirpath.split("/") if s.strip()]
    for i in range(len(folders)):
        parent = "/".join(folders[:i])
        if len(parent) <= 0:
            parent = "/"
        else:
            parent = "/" + parent + "/"
        folder_info.parents.append(parent)
    # print(f"parents-> {folder_info.parents}")
    
    # gether folder information
    for entry in os.listdir(dir_fullpath):
        entry_fullpath = os.path.join(dir_fullpath, entry)
        if os.path.isdir(entry_fullpath):
            folder_info.children.append(entry + "/")
        elif os.path.isfile(entry_fullpath):
            folder_info.files.append(entry)

    return folder_info

# ---------------------------------------------------------
# move folder

class FolderMove(BaseModel):
    move_from: str  # fullpath
    move_to: str    # fullpath

@app.post("/folder/move", tags=["folders"])
async def move_folder(param: FolderMove) -> FolderResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")

    # normalize target path
    src_path = os.path.abspath(basepath + param.move_from)
    dst_path = os.path.abspath(basepath + param.move_to)

    # check path trajectory
    if not src_path.startswith(basepath):
        return FolderResult(
            folder_path=src_path,
            succeed=False,
            message="src path trajectory failure.")
    if not dst_path.startswith(basepath):
        return FolderResult(
            folder_path=src_path,
            succeed=False,
            message="dst path trajectory failure.")

    # same path error
    if src_path == dst_path:
        return FolderResult(
            folder_path=param.move_from,
            succeed=False,
            message="source and destination are same")

    # source exist check
    if not os.path.isdir(src_path):
        return FolderResult(
            folder_path=param.move_from,
            succeed=False,
            message="source folder not exists")

    # destination not exist check
    if os.path.exists(dst_path):
        return FolderResult(
            folder_path=param.move_to,
            succeed=False,
            message="destination already exists")

    try:
        # フォルダの移動実行
        shutil.move(src_path, dst_path)
        return FolderResult(
            folder_path=param.move_to,
            succeed=True,
            message="folder moved successfully")
    except Exception as e:
        return FolderResult(
            folder_path=param.move_from,
            succeed=False,
            message=f"move failed: {str(e)}")

# ---------------------------------------------------------
# delete folder

class FolderDelete(BaseModel):
    folder_path: str # fullpath

@app.delete("/folder/delete", tags=["folders"])
async def delete_folder(param: FolderDelete) -> FolderResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")

    # normalize target path
    target_path = os.path.abspath(basepath + param.folder_path)

    # check path trajectory
    if not target_path.startswith(basepath):
        return FolderResult(
            folder_path=param.folder_path,
            succeed=False,
            message="path trajectory failure")

    # check if folder exists
    if not os.path.isdir(target_path):
        return FolderResult(
            folder_path=param.folder_path,
            succeed=False,
            message="folder not exists")

    try:
        # delete folder and all contents recursively
        shutil.rmtree(target_path)
        return FolderResult(
            folder_path=param.folder_path,
            succeed=True,
            message="folder deleted successfully")
    except Exception as e:
        return FolderResult(
            folder_path=param.folder_path,
            succeed=False,
            message=f"delete failed: {str(e)}")


# ---------------------------------------------------------
# create file
class FileResult(BaseModel):
    file_path: str
    succeed: bool
    message: str

class FileCreate(BaseModel):
    parent: str # path
    name: str   # need extension


@app.post("/file/create", tags=["files"])
async def create_file(param: FileCreate) -> FileResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")
    fullwikipath = param.parent + param.name
    
    # return if folder name is empty or wrong format
    if not valid_basename(param.name):
        return FileResult(
            file_path=fullwikipath,
            succeed=False, 
            message="file name is wrong format")

    # check parent exists
    parent_path = os.path.abspath(basepath + param.parent)
    print(f"create parent -> {parent_path}")
    if not os.path.isdir(parent_path):
        return FileResult(
            file_path=fullwikipath,
            succeed=False,
            message="parent folder not found")

    # error if already exists
    new_file_path = os.path.join(parent_path, param.name)
    print(f"new file path -> {new_file_path}")
    if os.path.isdir(new_file_path):
        return FileResult(
            file_path=fullwikipath,
            succeed=False,
            message="already exists")

    # check path trajectory
    if not new_file_path.startswith(basepath):
        return FileResult(
            file_path=fullwikipath,
            succeed=False,
            message="path trajectory failure.")

    # create empty file
    with open(new_file_path, "wb") as f:
        f.write(b"")
    return FileResult(file_path=fullwikipath, succeed=True, message="File created successfully")

# ---------------------------------------------------------
# get content
class FileDetail(BaseModel):
    parent: str # path
    fullpath: str
    name: str   # need extension
    content_type: str | None
    contents: str | None

@app.get("/file/detail", tags=["files"])
async def get_file(filepath: str) -> FileDetail | FileResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")
    actual_path = os.path.abspath(basepath + filepath)

    # check path trajectory
    if not actual_path.startswith(basepath):
        return FileResult(
            file_path=filepath,
            succeed=False,
            message="path check failure")

    # check file exists
    print(f"target filepath -> {actual_path}")
    if not os.path.exists(actual_path):
        return FileResult(
            file_path=filepath,
            succeed=False,
            message="file not exists")

    # get whole content
    detail = FileDetail(
        parent=os.path.dirname(filepath),
        fullpath=filepath,
        name=os.path.basename(filepath),
        content_type=None,  # TODO : fix type
        contents=None)

    with open(actual_path, "rt", encoding="utf-8") as f:
        detail.contents = f.read()

    return detail

# ---------------------------------------------------------
# move file

class FileRename(BaseModel):
    move_from: str
    move_to: str

@app.post("/file/move", tags=["files"])
async def rename_file(param: FileRename) -> FileResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")

    # check old path trajectory
    old_actual_path = os.path.abspath(basepath + param.move_from)
    if not old_actual_path.startswith(basepath):
        return FileResult(
            file_path=param.move_from,
            succeed=False, 
            message="old path trajectory check failure")

    # check new path trajectory
    new_actual_path = os.path.abspath(basepath + param.move_to) 
    if not new_actual_path.startswith(basepath):
        return FileResult(
            file_path=param.move_to,
            succeed=False,
            message="new path trajectory check failure")

    # check old file exists
    if not os.path.isfile(old_actual_path):
        return FileResult(
            file_path=param.move_from,
            succeed=False,
            message="source file not exists")

    # check new path not exists
    if os.path.isfile(new_actual_path):
        return FileResult(
            file_path=param.move_to, 
            succeed=False,
            message="target path already exists")

    # rename file
    os.rename(old_actual_path, new_actual_path)

    return FileResult(
        file_path=param.move_to,
        succeed=True,
        message="file renamed successfully")


# ---------------------------------------------------------
# delete file
class FileDelete(BaseModel):
    filepath: str

@app.delete("/file/delete", tags=["files"])
async def delete_file(param: FileDelete) -> FileResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")

    # check path trajectory
    actual_path = os.path.abspath(basepath + param.filepath)
    if not actual_path.startswith(basepath):
        return FileResult(
            file_path=param.filepath,
            succeed=False,
            message="path trajectory check failure")

    # check file exists
    if not os.path.isfile(actual_path):
        return FileResult(
            file_path=param.filepath,
            succeed=False,
            message="file not exists")

    # delete file
    os.remove(actual_path)

    return FileResult(
        file_path=param.filepath,
        succeed=True,
        message="file deleted successfully")



# ---------------------------------------------------------
# put content
class FileContent(BaseModel):
    fullpath: str
    content_type: str | None
    contents: str | None
    tags: str | None

@app.put("/file/update", tags=["files"])
async def update_file(param: FileContent) -> FileResult:
    basepath = os.path.abspath(os.getenv("WIKI_DIR"))
    print(f"wiki basepath -> {basepath}")
    fullwikipath = param.fullpath

    # check path trajectory
    actual_path = os.path.abspath(basepath + fullwikipath)
    print(f"actual path -> {actual_path}")
    if not actual_path.startswith(basepath):
        return FileResult(
            file_path=fullwikipath,
            succeed=False,
            message="path trajectory failure.")

    # exist check
    if not os.path.isfile(actual_path):
        return FileResult(
            file_path=fullwikipath,
            succeed=False,
            message="file not exists, create file first.")

    # update file
    with open(actual_path, "wt", encoding="utf-8") as f:
        f.write(param.contents)
    
    return FileResult(
        file_path=fullwikipath,
        succeed=True,
        message="file updated.")
