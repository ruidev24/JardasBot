import sqlite3


############################################################
def test_code():
    try:
        conn = sqlite3.connect("wordstats.db")
        print(conn)
        c = conn.cursor()

        c.execute(
        """UPDATE global_variables 
            SET death_roll = 100
            WHERE id = 1
        """
        )

        conn.commit()
    except sqlite3.Error as e:
        print("Error executing:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    test_code()
