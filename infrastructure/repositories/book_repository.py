import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def getAllBooks():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()

    books_result = []

    for row in books:
        books_result.append({"id":row['id'], "title": row['title'], "writer": row['writer'], "created": row['created']})

    return books_result

def getBookById(id):
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchall()
    conn.close()

    for row in books:
        return {"id":row['id'], "title": row['title'], "writer": row['writer'], "created": row['created']}
    
def updateBook(request, id):
    conn = get_db_connection()
    conn.execute('UPDATE books set title = ?, writer = ? WHERE id = ?', (request.get("title"), request.get("writer"), id,))
    conn.commit()
    conn.close()
    return getBookById(id)

def insertBook(request):
    conn = get_db_connection()
    conn.execute("INSERT INTO books (title, writer, created) VALUES (?, ?, ?)", (request.get("title"), request.get("writer"), datetime.now()))
    conn.commit()
    conn.close()

def deleteBook(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
