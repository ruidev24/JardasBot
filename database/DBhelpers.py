import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE = os.getenv("DATABASE")

##############################################################################
def db_select_one(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(query, params)
        return c.fetchone()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def db_select_all(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(query, params)
        return c.fetchall()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def db_execute_query(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()