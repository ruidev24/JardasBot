import sqlite3


############################################################
def test_code():
    try:
        conn = sqlite3.connect("wordstats.db")
        print(conn)
        c = conn.cursor()

        c.execute(
        """DELETE FROM nuke_table
        """
        )

        conn.commit()
    except sqlite3.Error as e:
        print("Error executing:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    test_code()
