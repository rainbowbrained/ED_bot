'''
функции подключения и работы с базой данных. 
Данный файл будет являться абстракцией базы данных от основного кода
'''
import sqlite3
import config 
from datetime import datetime
from aiogram.fsm.context import FSMContext

def drop_db(path_db : str):
    try:
        sqlite_connection = sqlite3.connect(path_db)
        sqlite_create_table_query = '''DROP TABLE IF EXISTS users;'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def create_db(path_db : str):
    try:
        sqlite_connection = sqlite3.connect(path_db)
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    gender TEXT,
                                    age INTEGER,
                                    weight INTEGER,
                                    height INTEGER,
                                    score1 INTEGER,
                                    score2 INTEGER,
                                    diagnosis TEXT,
                                    sleep_tracker INTEGER,
                                    water_tracker INTEGER,
                                    water_reminder INTEGER, 
                                    food_reminder INTEGER, 
                                    state_reminder INTEGER, 
                                    sleep_reminder INTEGER,
                                    end_subscription datetime,
                                    joining_date datetime);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def user_in_db (user_id : str):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?;", (user_id, ))
        data = cursor.fetchone()
        res = True
        if data is None:
            res = False
        con.commit()
        con.close()
        return res

    except sqlite3.Error as error:
        print("!Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")


def add_user_to_db (user_id : str, name : str):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?;", (user_id, ))
        data = cursor.fetchone()
        if data is None:
            print('There is no component named')
            new_user = (user_id, name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute("INSERT INTO users (id, name, joining_date) VALUES (?, ?, ?)", new_user)
        else:
            print('Component found with rowid %s'%data[0])
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")

async def edit_user_db (user_id, data):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?;", (user_id, ))
        data1 = cursor.fetchone()
        if data1 is None:
            print('There is no component named')
            new_user = (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute("INSERT INTO users (id, joining_date) VALUES (?, ?)", new_user)
        else:
            print('Component found with rowid %s'%data1[0])
        print(data1)
        cursor.execute("UPDATE users SET gender=?, age=?, height=?, weight=?  WHERE id=?", 
                           (data['gender'], data['age'], data['height'], data['weight'], user_id))
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")

async def edit_user_db_score (user_id, score1, score2):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?;", (user_id, ))
        data1 = cursor.fetchone()
        if data1 is None:
            print('There is no component named')
            new_user = (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute("INSERT INTO users (id, joining_date) VALUES (?, ?)", new_user)
        else:
            print('Component found with rowid %s'%data1[0])
        print(data1)
        cursor.execute("UPDATE users SET score1=?, score2=? WHERE id=?", 
                           (score1, score2, user_id))
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")

def get_user_db (user_id):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT name, gender, age, height, weight FROM users WHERE id=?", (user_id, ))
        data = cursor.fetchone()
        con.commit()
        con.close()
        return data
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")

def get_user_db_score (user_id):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT score1, score2 FROM users WHERE id=?", (user_id, ))
        data = cursor.fetchone()
        con.commit()
        con.close()
        return data
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")

#-------------------------------------------------USER DAILY------------------------
#total consumed water, sleep, food
def create_db_daily():
    try:
        sqlite_connection = sqlite3.connect(config.DB_PATH_daily)
        sqlite_create_table_query = '''CREATE TABLE users_daily (
                                    id INTEGER,
                                    date datetime,
                                    water INTEGER,
                                    start_time INTEGER,
                                    finish_time INTEGER,
                                    food_summary TEXT);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица daily создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def add_user_daily (user_id : str):
    try:
        con = sqlite3.connect(config.DB_PATH_daily)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users_daily WHERE id=? AND date = ?;", (user_id, datetime.now().strftime('%Y-%m-%d'),  ))
        data = cursor.fetchone()
        if data is None:
            print('There is no component named')
            new_line = (user_id, datetime.now().strftime('%Y-%m-%d'))
            cursor.execute("INSERT INTO users (id, date) VALUES (?, ?, ?)", new_line)
        else:
            print('Component found with rowid %s'%data[0])
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")


def add_water (user_id : str, volume : int):
    try:
        con = sqlite3.connect(config.DB_PATH_daily)
        cursor = con.cursor()
        cursor.execute("SELECT water FROM users_daily WHERE id=? AND date = ?;", (user_id, datetime.now().strftime('%Y-%m-%d'),  ))
        data = cursor.fetchone()
        if data is None:
            print('There is no component named')
            add_user_daily(user_id)
            data = 0
        cursor.execute("UPDATE users_daily SET water=?  WHERE id=? AND date = ?", 
                       (volume + data, user_id, datetime.now().strftime('%Y-%m-%d'),  ))
                        
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")



#-------------------------------------------------USER ACHIEVEMENTS------------------------
def create_db_achievements():
    try:
        sqlite_connection = sqlite3.connect(config.DB_PATH_achievements)
        sqlite_create_table_query = '''CREATE TABLE users_achievements (
                                    id INTEGER PRIMARY KEY,  
                                    time_with_bot INTEGER,
                                    time_showed_up INTEGER,
                                    time_prevent_breakdown INTEGER,
                                    quantity_practices INTEGER,
                                    time_without_overeating INTEGER,
                                    time_without_compensations INTEGER,
                                    log_water_day INTEGER,
                                    log_sleep_day INTEGER,
                                    log_food_day INTEGER,
                                    days_good_mood INTEGER,
                                    days_good_food INTEGER,
                                    days_good_water INTEGER,
                                    days_good_sleep INTEGER);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица daily создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к users_achievements", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с users_achievements закрыто")


def add_user_achievements (user_id : str):
    try:
        con = sqlite3.connect(config.DB_PATH_daily)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users_achievements WHERE id=?;", (user_id,  ))
        data = cursor.fetchone()
        if data is None:
            print('There is no component named')
            new_line = (user_id,)
            cursor.execute("INSERT INTO users (id) VALUES (?, )", new_line)
        else:
            print('Component found with rowid %s'%data[0])
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")


def add_achievement (vals):
    try:
        con = sqlite3.connect(config.DB_PATH_daily)
        cursor = con.cursor()
        cursor.execute("SELECT water FROM users_achievements WHERE id=?;", (vals[-1], ))
        data = cursor.fetchone()
        if data is None:
            print('There is no component named')
            add_user_achievements(vals[-1])
            data = 0
        cursor.execute("UPDATE users_achievements SET time_with_bot =? time_showed_up =? \
                                    time_prevent_breakdown =? \
                                    quantity_practices =?\
                                    time_without_overeating =?\
                                    time_without_compensations =?\
                                    log_water_day=? \
                                    log_sleep_day=? \
                                    log_food_day=? \
                                    days_good_mood =? \
                                    days_good_food=? \
                                    days_good_water =? \
                                    days_good_sleep=? \
                                      WHERE id=?", vals)

                       
        con.commit()
        con.close()
        return

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")


def get_user_db_achievemnts (user_id):
    try:
        con = sqlite3.connect(config.DB_PATH)
        cursor = con.cursor()
        cursor.execute("SELECT time_with_bot =? time_showed_up =? \
                                    time_prevent_breakdown =? \
                                    quantity_practices =?\
                                    time_without_overeating =?\
                                    time_without_compensations =?\
                                    log_water_day=? \
                                    log_sleep_day=? \
                                    log_food_day=? \
                                    days_good_mood =? \
                                    days_good_food=? \
                                    days_good_water =? \
                                    days_good_sleep=? \
                                    FROM users_achievements WHERE id=?", user_id)
        data = cursor.fetchone()
        con.commit()
        con.close()
        return data
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (con):
            con.close()
            print("Соединение с SQLite закрыто")


'''
try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_insert_query = """INSERT INTO sqlitedb_developers
                          (id, name, email, joining_date, salary)
                          VALUES (4, 'Alex', 'sale@gmail.com', '2020-11-20', 8600);"""
    cursor.execute(sqlite_insert_query)

    sql_update_query = """Update sqlitedb_developers set salary = 10000 where id = 4"""
    cursor.execute(sql_update_query)

    sql_delete_query = """DELETE from sqlitedb_developers where id = 4"""
    cursor.execute(sql_delete_query)

    sqlite_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if (sqlite_connection):
        print("Всего строк, измененных после подключения к базе данных: ", sqlite_connection.total_changes)
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
'''