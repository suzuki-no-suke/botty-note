from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

# 1. ファイルの取得
class FileRetrieveResponse(BaseModel):
    """ファイルデータ取得"""
    file_path: str  # ファイルパス（拡張子まで）
    content_type: str  # ContentType（MIME）
    content: Optional[dict]  # コンテンツ（ContentTypeに合わせたデータ）
    # 以下DBから取得
    id: int  # ID（DBから取得）
    wikiname: str  # Wikiname（DBから取得）
    created_at: datetime  # CreatedAt
    updated_at: datetime  # UpdatedAt
    tags: List[str]  # タグ

# 2. ファイルの追加・更新
class FileUpdateRequest(BaseModel):
    """ファイルの更新（移動を除く）"""
    file_path: str  # ファイルパス（必須）
    wikiname: Optional[str]  # Wikiname（あったら更新）
    content_type: Optional[str]  # ContentType（あったら更新）
    tags: Optional[List[str]]  # タグ（あったら更新）
    content: Optional[dict]  # コンテンツ（あったら更新）

# 3. ファイルの削除
class FileDeleteRequest(BaseModel):
    """ファイルの削除"""
    file_path: str  # ファイルパス（必須）

# 4. ファイルの移動
class FileMoveRequest(BaseModel):
    """ファイルの移動"""
    old_file_path: str  # 移動前ファイルパス（必須）
    moved_file_path: str # 移動後ファイルパス（必須）

# 5. 戻り値・共通
class FileOperateResponse(BaseModel):
    """ファイル操作の結果"""
    updated_file_path: str # NOTE : move の場合特に移動後
    succeed: bool
    message: str


