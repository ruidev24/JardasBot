from database.DBhelpers import db_execute_query, db_select_all, db_select_one


def update_channels(channel):
    channel_str = str(channel)
    query = """INSERT INTO channels (name)
                VALUES (?)
                ON CONFLICT (name)
                DO NOTHING
            """
    db_execute_query(query, (channel_str,))


def update_users(member):
    username = str(member)
    nick = str(member.nick) if member.nick else username
    mention = member.mention

    query = """INSERT INTO users (username, server_nick, mention)
                            VALUES (?, ?, ?)
                            ON CONFLICT (username)
                            DO NOTHING
                        """
                
    db_execute_query(query, (username, nick, mention))


def update_favour_table(member):
    username = str(member)
    query = """INSERT INTO favour_table (username, favour)
                VALUES (?, 0)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


def update_fortune_table(member):
    username = str(member)
    query = """INSERT INTO fortune_table (username, allowed)
                VALUES (?, True)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))



def update_mention_bot_table(member):
    username = str(member)
    query = """INSERT INTO mention_bot_table (username, mention_count)
                VALUES (?, 0)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


def update_nuke_table(member):
    username = str(member)
    query = """INSERT INTO nuke_table (username, nuke_count, defuse_count, allowed)
                VALUES (?, 0, 0, True)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


# DONT USE THIS ONE
def update_highscores_table(member):
    username = str(member)
    query = """INSERT INTO highscores (username)
                VALUES (?)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


def setup_global_variables():
    query = """INSERT INTO global_variables (state, intensity, message_count, death_roll)
                VALUES(1, 1, 1, 100)"""
    

def clean_data():
    queries = [
            "DELETE FROM channel_words",
            "DELETE FROM channels",
            "DELETE FROM favour_table",
            "DELETE FROM fortune_table",
            "DELETE FROM global_variables",
            "DELETE FROM highscores",
            "DELETE FROM mention_bot_table",
            "DELETE FROM nuke_table",
            "DELETE FROM user_words",
            "DELETE FROM users",
            "DELETE FROM vocabulary_table",
            "DELETE FROM words"
        ]

    for query in queries:
            db_execute_query(query)

def clean_words():
    query = """DELETE FROM words"""
    db_execute_query(query)