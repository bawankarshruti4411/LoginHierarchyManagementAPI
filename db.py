import mysql.connector
import os

def get_db():
    db = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor
