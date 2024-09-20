import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def getAllBooks():
    conn = get_db_connection()
    try:
        books = conn.execute('SELECT * FROM books').fetchall()
        books_result = [{"id": row['id'], "title": row['title'], "writer": row['writer'], "created": row['created']} for row in books]
    finally:
        conn.close()
    return books_result

def getBookById(id):
    conn = get_db_connection()
    try:
        book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
        if book:
            return {"id": book['id'], "title": book['title'], "writer": book['writer'], "created": book['created']}
        else:
            return None
    finally:
        conn.close()

def updateBook(request, id):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE books SET title = ?, writer = ? WHERE id = ?', 
                     (request.get("title"), request.get("writer"), id))
        conn.commit()
        return getBookById(id)
    finally:
        conn.close()

def insertBook(request):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO books (title, writer, created) VALUES (?, ?, ?)",
                     (request.get("title"), request.get("writer"), datetime.now()))
        conn.commit()
    finally:
        conn.close()

def deleteBook(id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM books WHERE id = ?", (id,))
        conn.commit()
    finally:
        conn.close()
