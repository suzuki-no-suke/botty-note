import os
from dotenv import load_dotenv

if __name__ == '__main__':
    # set db abs path
    load_dotenv("../.env")
    DB_CONN = os.getenv('DB_CONN')
    print(f"db connection -> {DB_CONN}")
    db_file = DB_CONN.replace('sqlite:///', '')

    rootdir = os.path.dirname(os.path.dirname(__file__))
    db_file = os.path.abspath(os.path.join(rootdir, db_file))
    print(f"db abs path -> {db_file}")

    # load and init_database
    if os.path.exists(db_file):
        os.remove(db_file)
    with open(db_file, 'w') as f:
        pass
    print("db reset")

    from .init_database import *
    print("init database finished")

    print("initialize completed")
