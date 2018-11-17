import psycopg2
from res import id as id, constants as constants


def insert_strategy(key, time_frame, strategy_name, time):
    connection = psycopg2.connect(constants.database[id.db_url])
    cur = connection.cursor()
    cur.execute("insert into strategy_filter (key,time_frame,strategy_name,time) values ({},{},{},{});"
                .format(key, time_frame, strategy_name, time))
    connection.commit()
