import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Svelteのデフォルトポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



import uuid
import re

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
    if not param.name or not re.match(r'^[a-zA-Z0-9_\-]+$', param.name):
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
    if not param.name or not re.match(r'^[a-zA-Z0-9_\-\.]+$', param.name):
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


"""

# ---------------------------------------------------------
# Folder処理
@app.post("/folders/", response_model=Folder)
def add_folder(folder: Folder):
    folders.append(folder)
    return folder

@app.put("/folders/{folder_id}", response_model=Folder)
def update_folder(folder_id: int, folder: Folder):
    for idx, f in enumerate(folders):
        if f.id == folder_id:
            folders[idx] = folder
            return folder
    raise HTTPException(status_code=404, detail="Folder not found")

@app.delete("/folders/{folder_id}")
def delete_folder(folder_id: int):
    global folders
    folders = [f for f in folders if f.id != folder_id]
    return {"message": "Folder deleted"}

@app.get("/folders/", response_model=List[Folder])
def list_folders():
    return folders

# ---------------------------------------------------------
# Page処理
@app.post("/pages/", response_model=Page)
def add_page(page: Page):
    pages.append(page)
    return page

@app.put("/pages/{page_id}", response_model=Page)
def update_page(page_id: int, page: Page):
    for idx, p in enumerate(pages):
        if p.id == page_id:
            pages[idx] = page
            return page
    raise HTTPException(status_code=404, detail="Page not found")

@app.delete("/pages/{page_id}")
def delete_page(page_id: int):
    global pages
    pages = [p for p in pages if p.id != page_id]
    return {"message": "Page deleted"}

@app.get("/pages/{page_id}", response_model=Page)
def get_page(page_id: int):
    for p in pages:
        if p.id == page_id:
            return p
    raise HTTPException(status_code=404, detail="Page not found")

# ---------------------------------------------------------
# Resource処理
@app.post("/resources/", response_model=Resource)
def add_resource(resource: Resource):
    resources.append(resource)
    return resource

@app.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: Resource):
    for idx, r in enumerate(resources):
        if r.id == resource_id:
            resources[idx] = resource
            return resource
    raise HTTPException(status_code=404, detail="Resource not found")

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int):
    global resources
    resources = [r for r in resources if r.id != resource_id]
    return {"message": "Resource deleted"}

@app.get("/resources/", response_model=List[Resource])
def list_resources():
    return resources

@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: int):
    for r in resources:
        if r.id == resource_id:
            return r
    raise HTTPException(status_code=404, detail="Resource not found")

"""
