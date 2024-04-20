import sqlite3

connection = sqlite3.connect('database.db')

with open('script.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO books (title, writer, created) VALUES (?, ?, ?)", ('Código limpo: habilidades práticas do Agile software', 'Robert C. Martin', '2024-04-19 19:40:00'))
cur.execute("INSERT INTO books (title, writer, created) VALUES (?, ?, ?)", ('Arquitetura limpa: o guia do artesão para estrutura e design de software', 'Robert C. Martin', '2024-04-19 19:40:00'))
cur.execute("INSERT INTO books (title, writer, created) VALUES (?, ?, ?)", ('Desenvolvimento ágil limpo: de volta às origens: Volume 1', 'Robert C. Martin', '2024-04-19 19:40:00'))

connection.commit()
connection.close()