import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def authenticateUser(request):
    conn = get_db_connection()
    try:
        # Use fetchone() since we're expecting a single result
        user = conn.execute(
            'SELECT * FROM users WHERE email = ? AND senha = ?',
            (request.get("email"), request.get("password"))
        ).fetchone()
    finally:
        conn.close()

    if user:
        # Return user data if found
        return {
            "nome": user['nome'],
            "email": user['email'],
            "id": user['id']
        }
    else:
        # Return None or an empty dictionary if not found
        return None

def insertUser(request):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
            (request.get("name"), request.get("email"), request.get("password"))
        )
        conn.commit()
    finally:
        conn.close()
