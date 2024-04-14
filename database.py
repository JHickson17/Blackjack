import sqlite3

connection = sqlite3.connect("database.db")
connection.execute("PRAGMA foreign_keys = 1")

cur = connection.cursor()

def create_users_table():   #Creates the table that stores the users login details and money
    cur.execute("""CREATE TABLE Users   
(Username TEXT PRIMARY KEY,
Password  TEXT,
Money     INTEGER)""") 

def create_statistics_table():  #Creates table that stores user's statistics with the username as a foreign key
    cur.execute("""CREATE TABLE Statistics
(Username       TEXT,
RoundsPlayed    INTEGER,
RoundsWon       INTEGER,
RoundsLost      INTEGER,
RoundsDrawn     INTEGER,
FOREIGN KEY (Username) REFERENCES Users (Username))""")


def add_user(username, password, money):    #Adds a new user to the database
    cur.execute("""INSERT INTO Users 
                   VALUES (?, ?, ?)""", (username, password, money))
    cur.execute("""INSERT INTO Statistics 
                   VALUES (?, ?, ?, ?, ?)""", (username, 0, 0, 0, 0))
    connection.commit()

def delete_record(username):    #Deletes a record from the database
    cur.execute("""DELETE FROM Users 
                   WHERE Username = ?""", (username,))
    connection.commit()

def find_user(username):    #Finds a user and returns their username, password and money
    cur.execute("""SELECT *
                   FROM Users 
                   WHERE Username=?""", (username,))
    userDetails = cur.fetchall()
    return userDetails

def update_money(username, money):  #Updates a user's money in the database
    cur.execute("""UPDATE Users 
                   SET   Money = ? 
                   WHERE Username = ?""", (money, username))
    connection.commit()

def load_leaderboard(): #Returns all users ordered by money
    cur.execute("""SELECT Username, Money
                   FROM   Users
                   ORDER BY Money DESC""")
    leaderboard = cur.fetchall()
    return leaderboard

def update_statistics(username, roundsPlayed, roundsWon, roundsLost, roundsDrawn):  #Updates a user's statistics
    cur.execute("""UPDATE Statistics 
                   SET (RoundsPlayed, RoundsWon, RoundsLost, RoundsDrawn) = (?, ?, ?, ?) 
                   WHERE Username = ?""", (roundsPlayed, roundsWon, roundsLost, roundsDrawn, username))
    connection.commit()

def load_statistics(username):  #Returns a user's statistics
    cur.execute("""SELECT roundsPlayed, roundsWon, roundsLost, roundsDrawn
                   FROM   Statistics
                   WHERE Username = ?""", (username,))
    statistics = cur.fetchall()
    return statistics
