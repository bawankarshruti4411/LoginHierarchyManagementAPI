import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import os

db_pool = MySQLConnectionPool(
    pool_name="hierarchy_pool",
    pool_size=10,
    host=os.environ.get("DB_HOST"),
    port=int(os.environ.get("DB_PORT", 16398)),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)

def get_db():
    db = db_pool.get_connection()
    cursor = db.cursor(dictionary=True)
    return db, cursor
