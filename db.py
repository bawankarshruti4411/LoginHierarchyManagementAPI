import mysql.connector

def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="hierarchy_db"
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor
