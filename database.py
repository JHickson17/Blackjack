import sqlite3

connection = sqlite3.connect("database.db")

cur = connection.cursor()

def create_table():
    cur.execute("CREATE TABLE people (Username TEXT, Password TEXT, Money INTEGER)")


def add_user(username, password, money):
    cur.execute("INSERT INTO Users VALUES (?, ?, ?)", (username, password, money))
    connection.commit()

def delete_record(username):
    cur.execute("DELETE FROM Users WHERE Username = ?", (username,))
    connection.commit()

def find_user(username):
    cur.execute("SELECT * FROM Users WHERE Username=?", (username,))
    userDetails = cur.fetchall()
    return userDetails

def update_money(username, money):
    cur.execute("UPDATE Users SET Money = ? WHERE Username = ?", (money, username))
    connection.commit()


