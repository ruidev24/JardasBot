import sqlite3
from utils.state import STATE
from database.DBhelpers import db_execute_query, db_select_all, db_select_one

def get_nuke_cnt():
    result = db_select_one("""SELECT SUM(nuke_count) - SUM(defuse_count) FROM nuke_table""")
    return result[0] if result else None

def get_intentsity():
    result = db_select_one("""SELECT intensity FROM global_variables WHERE id = 1""")
    return result[0] if result else None


def update_intensity(intensity):
    query = """UPDATE global_variables
               SET intensity = ?
               WHERE id = 1
            """
    db_execute_query(query, (intensity,))


def get_state():
    result = db_select_one("""SELECT state FROM global_variables WHERE id = 1""")
    return result[0] if result else None


def update_state(state: STATE):
    query = """UPDATE global_variables
               SET state = ?
               WHERE id = 1
            """
    db_execute_query(query, (state.value,))


def get_death_roll():
    result = db_select_one("""SELECT death_roll FROM global_variables WHERE id = 1""")
    return result[0] if result else None

def update_death_roll(death_roll):
    query = """UPDATE global_variables
                SET death_roll = ?
                WHERE id = 1
            """
    
    db_execute_query(query, (death_roll,))

