import os
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

# ==========================================
# CONNECTION POOL
# psycopg2's pool works a bit differently from mysql-connector's:
# - minconn / maxconn instead of a single pool_size
# - getconn() / putconn() instead of get_connection()
# ==========================================

db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.environ.get("DB_HOST"),
    port=int(os.environ.get("DB_PORT", 5432)),  # Neon default port is 5432, not 16398
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    dbname=os.environ.get("DB_NAME"),
    sslmode="require",  # Neon requires SSL — MySQL/Railway setup didn't need this
)


def get_db():
    """
    Returns (db, cursor) just like before.
    dictionary=True in mysql.connector becomes cursor_factory=RealDictCursor here —
    both return rows as dicts instead of tuples.
    """
    db = db_pool.getconn()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    return db, cursor


def release_db(db):
    """
    IMPORTANT — new step that MySQL's pool didn't require you to think about.
    mysql-connector automatically returns connections to the pool when closed.
    psycopg2 does NOT — you must explicitly call putconn(), or the pool
    runs out of connections and every request starts hanging.
    Call this in a `finally` block everywhere you call get_db().
    """
    db_pool.putconn(db)
