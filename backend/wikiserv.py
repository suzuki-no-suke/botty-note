import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

import uuid

# really implemented
# ---------------------------------------------------------

class FolderTreeNode(BaseModel):
    """フォルダの入れ子関係を、フォルダIDのみ表示する"""
    id: str
    folders: List['FolderTreeNode'] = []

class Folder(BaseModel):
    """単一フォルダのデータを表示する"""
    fullpath: str # root = /, root to this folder
    id: str # uuid4
    name: str
    num_files: int
    children: List[str] = []    # only children folder id

def parse_folder(dirpath, wikipath="/"):
    folders = {}
    nid = str(uuid.uuid4())
    node = FolderTreeNode(id=nid, folders=[])
    this_folder = Folder(
        fullpath=wikipath,
        id=nid,
        name=os.path.basename(dirpath),
        num_files=0,
        children=[]
    )

    for name in os.listdir(dirpath):
        entry_path = os.path.join(dirpath, name)
        if os.path.isdir(entry_path):
            f, n = parse_folder(entry_path, wikipath + "/" + name)
            folders.update(f)
            print(folders)
            node.folders.append(n)
            this_folder.children.append(n.id)
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

    print(folders)
    print(tree)

    return FolderTree(all_folders=folders, root_node=tree)



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
