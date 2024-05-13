import sqlite3
from responses import BomDia
import random

############################################################
def clear_nuke_table():
    try:
        conn = sqlite3.connect("wordstats.db")
        print(conn)
        c = conn.cursor()
        
        # Delete nuke table
        c.execute("DELETE FROM favour_table WHERE username = ? ", ("ruimachado",))
        
        conn.commit()
    except sqlite3.Error as e:
        print("Error deleting tables from database:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    transformed_channel = clear_nuke_table()
    print(transformed_channel)
