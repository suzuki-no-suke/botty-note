# backend/wikiserv.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# ---------------------------------------------------------
# pydantic models

# Folderモデル
class Folder(BaseModel):
    id: int
    name: str

folders = []

# Pageモデル
class Page(BaseModel):
    id: int
    title: str
    content: str

pages = []

# Resourceモデル
class Resource(BaseModel):
    id: int
    name: str
    url: str

resources = []

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

