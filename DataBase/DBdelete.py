import sqlite3

############################################################
def clear_nuke_table():
    try:
        conn = sqlite3.connect("wordstats.db")
        print(conn)
        c = conn.cursor()
        
        # Delete nuke table
        c.execute("DELETE FROM nuke_table")
        
        conn.commit()
    except sqlite3.Error as e:
        print("Error deleting tables from database:", e)
    finally:
        conn.close()


#########################################################        
def delete_database():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        
        # Delete users table
        c.execute("DELETE FROM users")
        
        # Delete channels table
        c.execute("DELETE FROM channels")
        
        # Create words table
        c.execute("DELETE FROM words")
        
        # Create userwords table
        c.execute("DELETE FROM userwords")
        
        # Create channelwords table
        c.execute("DELETE FROM channelwords")
        
        conn.commit()
        print("Tables deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting tables from database:", e)
    finally:
        conn.close()
