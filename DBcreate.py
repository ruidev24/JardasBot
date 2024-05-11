import sqlite3

def create_database():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        
        # Create users table
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        server_nick TEXT
                    )""")
        
        # Create channels table
        c.execute("""CREATE TABLE IF NOT EXISTS channels (
                        channel_id INTEGER PRIMARY KEY,
                        channel_name TEXT
                    )""")
        
        # Create words table
        c.execute("""CREATE TABLE IF NOT EXISTS words (
                        word TEXT PRIMARY KEY,
                        count INTEGER
                    )""")
        
        # Create userwords table
        c.execute("""CREATE TABLE IF NOT EXISTS userwords (
                        username TEXT,
                        word TEXT,
                        count INTEGER,
                        FOREIGN KEY(username) REFERENCES users(username),
                        FOREIGN KEY(word) REFERENCES words(word),
                        PRIMARY KEY (username, word)
                    )""")
        
        # Create channelwords table
        c.execute("""CREATE TABLE IF NOT EXISTS channelwords (
                        channel_id INTEGER,
                        word TEXT,
                        count INTEGER,
                        FOREIGN KEY(channel_id) REFERENCES channels(channel_id),
                        FOREIGN KEY(word) REFERENCES words(word),
                        PRIMARY KEY (channel_id, word)
                    )""")
        
        # Create Favour User table
        c.execute("""CREATE TABLE IF NOT EXISTS favour_table (
                    username TEXT,
                    favour INTEGER,
                    FOREIGN KEY(username) REFERENCES users(username)
                )""")
        
        # Create Mention User table
        c.execute("""CREATE TABLE IF NOT EXISTS mention_table (
                    username TEXT,
                    mention_cnt INTEGER,
                    FOREIGN KEY(username) REFERENCES users(username)
                )""")
        
        # Create Nuke User table
        c.execute("""CREATE TABLE IF NOT EXISTS nuke_table (
                    username TEXT,
                    nuke_count INTEGER,
                    defuse_count INTEGER,
                    date DATETIME
                )""")
        
        # Create Vocabulary table
        c.execute("""CREATE TABLE IF NOT EXISTS vocabulary_table (
                  vocabulary TEXT,
                  username TEXT
                  )""")
        
        conn.commit()
        print("Database created successfully.")
    except sqlite3.Error as e:
        print("Error creating database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    print("Creating database...")
    create_database()
