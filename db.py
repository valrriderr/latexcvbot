import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            name TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            filename TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()

def add_user(telegram_id, name):
    cursor.execute("""
        INSERT INTO users (telegram_id, name)
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
    """, (telegram_id, name))
    conn.commit()

def add_resume(user_telegram_id, filename):
    cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_telegram_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("""
            INSERT INTO resumes (user_id, filename)
            VALUES (%s, %s);
        """, (user[0], filename))
        conn.commit()