# backend/src/datadef/folder.py

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class FolderTreeResponse(BaseModel):
    """Root からのフォルダツリー"""
    tree: dict

class FolderDetailResponse(BaseModel):
    """フォルダ内部詳細"""
    folder_path: str
    parent_folders: List[str]
    contents_entry: List[dict]
    created_at: datetime
    updated_at: datetime
    id: str
    wikiname: str
    tags: List[str]

class FolderUpdateRequest(BaseModel):
    """フォルダ情報更新"""
    folder_path: str
    wikiname: str
    tags: List[str]

class FolderMoveRequest(BaseModel):
    """フォルダ移動"""
    from_path: str
    to_path: str

class FolderDeleteRequest(BaseModel):
    """フォルダ削除（内部も削除）"""
    folder_path: str

class FolderProcessResult(BaseModel):
    """フォルダ操作結果"""
    updated_folder_path: str
    success: bool
    message: str
