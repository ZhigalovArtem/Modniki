import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('project.db')
    conn.row_factory = sqlite3.Row  # Для обращения к данным по имени столбца
    return conn

# Создание таблиц
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        birth_date TEXT,
        stylist BOOLEAN DEFAULT 0,
        level INTEGER DEFAULT 0,
        photo_path TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_parameters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        height REAL,
        weight REAL,
        chest_size REAL,
        ass_size REAL,
        waist_size REAL,
        clothes_size TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stylist_docs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        resume_path TEXT,
        diploma_path TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_chats (
        user_chats_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES user_chats(chat_id),
        FOREIGN KEY (creator_id) REFERENCES users(user_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_read_status (
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        last_read TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (chat_id, user_id),
        FOREIGN KEY (chat_id) REFERENCES user_chats(chat_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shmotki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        shmotka_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ''')



    conn.commit()
    conn.close()

# добавление пользователя
def add_user(first_name, last_name, password, email, birth_date, stylist, level, photo_path): # Добавить исключение и возвращение результата
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (first_name, last_name, password, email, birth_date, stylist, level, photo_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (first_name, last_name, password, email, birth_date, stylist, level, photo_path))
    conn.commit()
    conn.close()

# добавление параметров пользователя
def add_user_params(height, weight, chest_size, ass_size, waist_size, clothes_size, email):
    user_id=get_user_info_by_email(email)['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO user_parameters (user_id, height, weight, chest_size, ass_size, waist_size, clothes_size)
    VALUES(?, ?, ?, ?, ?, ?, ?) 
    ''',(user_id, height, weight, chest_size, ass_size, waist_size, clothes_size))

    conn.commit()
    conn.close()

# получение информации о пользователе по email
def get_user_info_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_info = cursor.fetchone()
    conn.close()
    return dict(user_info) if user_info else None

# получение информации о пользователе по id
def get_user_info_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_info = cursor.fetchone()
    conn.close()
    return dict(user_info) if user_info else None

def get_CL_list():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE stylist = 0')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_ST_list():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE stylist = 1')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users JOIN user_parameters ON users.user_id = user_parameters.user_id')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]