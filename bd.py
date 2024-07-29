import sqlite3


connection = sqlite3.connect('basa.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_user INTEGER,
username TEXT,
first_name TEXT NOT NULL,
task TEXT NOT NULL,
status INTEGER DEFAULT 0
)
''')


# Функция получения всего списка заданий пользователя
def get_all_tasks(id_user):
    cursor.execute('SELECT * FROM Tasks WHERE id_user = ?;', (id_user,))
    result = cursor.fetchall()
    connection.commit()
    return result


# Функция добавления задания пользователя
def add_task(id_user, username, first_name, task):
    cursor.execute('''
    INSERT INTO Tasks (id_user, username, first_name, task)
    VALUES (?, ?, ?, ?)
    ''', (id_user, username, first_name, task))
    connection.commit()


# Функция редактирования задания пользователя
def edit_task(id_, task):
    cursor.execute('''
    UPDATE Tasks SET task = ? WHERE id = ?
    ''', (task, id_))
    connection.commit()


# Функция удаления задания пользователя
def delete_task(id_):
    cursor.execute('''
    DELETE FROM Tasks WHERE id = ?
    ''', (id_,))
    connection.commit()
