from utils.state import STATE
from database.DBhelpers import db_execute_query, db_select_one


##############################################################################
def get_nuke_cnt() -> int:
    query = """SELECT SUM(nuke_count) - SUM(defuse_count) FROM nuke_table"""
    result = db_select_one(query)
    return result[0] if result else None


def get_intentsity() -> int:
    query = """SELECT intensity FROM global_variables WHERE id = 1"""
    result = db_select_one(query)
    return result[0] if result else None


def update_intensity(intensity):
    query = """UPDATE global_variables
               SET intensity = ?
               WHERE id = 1
            """
    db_execute_query(query, (intensity,))


def get_state() -> int:
    query = """SELECT state FROM global_variables WHERE id = 1"""
    result = db_select_one(query)
    return result[0] if result else None

def bot_is_sleeping():
    if STATE(get_state()) == STATE.SLEEP: 
        return True
    else:
        return False


def update_state(state: STATE):
    query = """UPDATE global_variables
               SET state = ?
               WHERE id = 1
            """
    db_execute_query(query, (state.value,))


def get_death_roll() -> int:
    query = """SELECT death_roll FROM global_variables WHERE id = 1"""
    result = db_select_one(query)
    return result[0] if result else None


def update_death_roll(death_roll):
    query = """UPDATE global_variables
                SET death_roll = ?
                WHERE id = 1
            """
    db_execute_query(query, (death_roll,))

