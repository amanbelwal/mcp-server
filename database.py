
import sqlite3

DB_FILE = "todos.db"


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_script = """
                 CREATE TABLE IF NOT EXISTS tasks 
                 ( 
                     id    INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title   TEXT NOT NULL, 
                     description TEXT, 
                     status  TEXT NOT NULL, 
                     due_date   TEXT, 
                     created_at  TEXT NOT NULL
                 );

                 CREATE TABLE IF NOT EXISTS subtasks 
                 ( 
                     id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     title   TEXT NOT NULL, 
                     status  TEXT NOT NULL, 
                     created_at  TEXT NOT NULL,
                     parent_task_id INTEGER NOT NULL, 
                     FOREIGN KEY (parent_task_id) REFERENCES tasks(id)
                 );
                 """

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()

init_db()