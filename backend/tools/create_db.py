import sqlite3
import os
from dotenv import load_dotenv

load_dotenv('../.env')
DB_CONN = os.getenv('DB_CONN')
print(f"db connected -> {DB_CONN}")

# when using sqlite3
db_file = DB_CONN.replace('sqlite:///', '')
print(f"db file -> {db_file}")
full_db_path = os.path.abspath(os.path.join("..", db_file))
print(f"db fullpath -> {full_db_path}")
conn = sqlite3.connect(full_db_path)
cur = conn.cursor()

# File system Meta
cur.execute('''
    CREATE TABLE IF NOT EXISTS file_system_meta (
        file_path TEXT PRIMARY KEY,
        type TEXT CHECK (entry_type IN ('file', 'directory')) NOT NULL,
        content_type TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        tag TEXT,
        unique_id TEXT,
        wikiname TEXT
    );
''')

conn.commit()
conn.close()