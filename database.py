import sqlite3

connection = sqlite3.connect("database.db")
connection.execute("PRAGMA foreign_keys = 1")

cur = connection.cursor()

def create_users_table():
    cur.execute("CREATE TABLE Users (Username TEXT PRIMARY KEY, Password TEXT, Money INTEGER)")

def create_statistics_table():
    cur.execute("""CREATE TABLE Statistics
(Username       INTEGER,
RoundsPlayed    TEXT,
RoundsWon       TEXT,
RoundsLost      TEXT,
RoundsDrawn     TEXT,
FOREIGN KEY (Username) REFERENCES Users (Username))""")
connection.commit()

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

