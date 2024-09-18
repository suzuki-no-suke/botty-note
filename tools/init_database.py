import sqlite3
import os
from dotenv import load_dotenv

load_dotenv("../.env")
DB_CONN = os.getenv('DB_CONN')
print(f"db connected -> {DB_CONN}")
db_file = DB_CONN.replace('sqlite:///', '')
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# CREATE TABLEs
cur.execute('''
    CREATE TABLE IF NOT EXISTS chatbot (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        botname TEXT NOT NULL,
        module_filename TEXT,
        classname TEXT
    );
''')

# chat_statusのENUMをTEXT型で代替
cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL,
        status TEXT CHECK(status IN ('waiting', 'in_progress', 'failed', 'completed')) NOT NULL,
        botname TEXT NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_message_list (
        history_id TEXT NOT NULL,
        message_id TEXT NOT NULL,
        time TIMESTAMP,
        PRIMARY KEY (history_id, message_id)
    );
''')

# chat_typeのENUMをTEXT型で代替
cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_message (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL,
        type TEXT CHECK(type IN ('human', 'user_meta', 'chatbot', 'bots_meta')) NOT NULL,
        content TEXT,
        time TIMESTAMP
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS file_content (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL,
        extension TEXT DEFAULT '',  -- 拡張子、ドット不要 (例: png, jpg, pdfなど)
        original_filename TEXT NOT NULL
    );
''')

conn.commit()
conn.close()