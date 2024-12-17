import sqlite3


############################################################
def test_code():
    try:
        conn = sqlite3.connect("wordstats.db")
        print(conn)
        c = conn.cursor()

        c.execute(
    """INSERT INTO global_variables (state, intensity)
        VALUES (1,3)
        """
)

        conn.commit()
    except sqlite3.Error as e:
        print("Error deleting tables from database:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    test_code()
