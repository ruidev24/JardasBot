import sqlite3


def execute_query(query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        if params is None:
            params = ()
        c.execute(query, params)

        if fetch_one:
            result = c.fetchone()
        elif fetch_all:
            result = c.fetchall()
        else:
            result = None

        conn.commit()
        return result
    except sqlite3.Error as e:
        print("Database error:", e)
        return None
    finally:
        conn.close()

def get_intentsity():
    result = execute_query(
        """SELECT intensity FROM global_variables WHERE id = 1""", fetch_one=True
    )
    return result if result else None


def update_intensity(intensity):
    query = """UPDATE TABLE global_variables
               SET intensity = ?
               WHERE id = 1
            """
    execute_query(query, (intensity,))


def get_state():
    result = execute_query(
        """SELECT state FROM global_variables WHERE id = 1""", fetch_one=True
    )
    return result[0] if result else None


def update_state(state):
    query = """UPDATE TABLE global_variables
               SET state = ?
               WHERE id = 1
            """
    execute_query(query, (state,))


def get_death_roll():
    result = execute_query(
        """SELECT death_roll FROM global_variables WHERE id = 1""", fetch_one=True
    )
    return result[0] if result else None

def update_death_roll(death_roll):
    query = """UPDATE global_variables
                SET death_roll = ?
                WHERE id = 1
            """
    
    execute_query(query, (death_roll,))