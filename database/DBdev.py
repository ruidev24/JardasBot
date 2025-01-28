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
    query = """INSERT INTO favour_table (username)
                VALUES (?)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


def update_fortune_table(member):
    username = str(member)
    query = """INSERT INTO fortune_table (username)
                VALUES (?)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))



def update_mention_bot_table(member):
    username = str(member)
    query = """INSERT INTO mention_bot_table (username)
                VALUES (?)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username,))


def update_nuke_table(member):
    username = str(member)
    query = """INSERT INTO mention_bot_table (username)
                VALUES (?)
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
    query = """INSERT INTO global_variables (intensity)
                VALUES(1)"""