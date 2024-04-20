import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def autenticateUser(request):
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users WHERE email = ? AND senha = ?',(request.get("email"),request.get("password"),)).fetchall()
    conn.close()

    for row in users:
        return {"nome":row['nome'], "email": row['email'], "id": row['id']}

def insertUser(request):
    conn = get_db_connection()
    conn.execute("INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)", (request.get("name"), request.get("email"), request.get("password")))
    conn.commit()
    conn.close()
