import os

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class DbSession:
    def __init__(self, dbobj):
        self.dbobj = dbobj
        self.session = None

    def __enter__(self):
        if self.session is not None:
            self.session.close()
            self.session = None
        session = sessionmaker(bind=self.dbobj.engine)()
        self.session = session
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session is not None:
            self.session.close()
            self.session = None

class SQLFactory:
    """SQLAlchemy の接続を管理するクラス"""
    def __init__(self, db_uri):
        self.db_uri = db_uri
        echoflag = os.getenv('DEBUG_QUERY_ECHO', False) == "True"
        self.engine = create_engine(self.db_uri, echo=echoflag)

    @classmethod
    def default_env(cls):
        """デフォルトの環境変数から接続を作成する"""
        db_uri = os.getenv("DB_CONN")
        return cls(db_uri)

    @classmethod
    def create_db(cls, conn_str);
        """指定された接続文字列を使って接続を作成する"""
        return cls(conn_str)

    def get_engine(self):
        return self.engine

    def get_new_session(self):
        return DbSession(self)
