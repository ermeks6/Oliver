import sqlite3


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("Database connected")

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY, "
               "username VARCHAR (100), "
               "name VARCHAR (100), "
               "age INTEGER, "
               "group_menty VARCHAR (10), "
               "direction VARCHAR (10))")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES (?, ?, ?, ?, ?, ?)",
                       tuple(data.values()))
        db.commit()



