# def cred():
#     from sqlalchemy import create_engine
#     import urllib
    
#     DB_CONFIG = {
#         'dbname': 'new_db',
#         'user': 'postgres',
#         'password': 'Strateena@check',
#         # 'host': '34.93.35.170',
#         'host': '118.150.8.0',
#         'port': 5432
#     }
    
#     def get_engine():
#         password = urllib.parse.quote_plus(DB_CONFIG['password'])
#         url = (
#             f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}"
#             f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
#         )
#         return create_engine(url)
        
#     return get_engine()

# import psycopg2
# from psycopg2.extras import RealDictCursor

# DB_CONFIG = {
#         'dbname': 'new_db',
#         'user': 'postgres',
#         'password': 'Strateena@check',
#         # 'host': '34.93.35.170',
#         'host': '118.150.8.0',
#         'port': 5432
#     }

# def db_query(query):
#     conn = None
#     try:
#         conn = psycopg2.connect(
#             dbname=DB_CONFIG['dbname'],
#             user=DB_CONFIG['user'],
#             password=DB_CONFIG['password'],
#             host=DB_CONFIG['host'],
#             port=DB_CONFIG['port']
#         )
#         with conn.cursor(cursor_factory=RealDictCursor) as cur:
#             cur.execute(query)
#             results = cur.fetchall()  # List of dicts
#         return results
#     except Exception as e:
#         print("Database query error:", e)
#         return []
#     finally:
#         if conn:
#             conn.close()

# def user_check():
#     users = db_query("SELECT first_name, last_name, username, email, password_hash FROM users")
#     creds = {"usernames": {}}
#     for user in users:
#         full_name = f"{user['first_name']} {user['last_name']}".strip()
#         creds["usernames"][user["username"]] = {
#             "name": full_name,
#             "email": user["email"],
#             "password": user["password_hash"]  # bcrypt-hashed passwords expected by streamlit-authenticator
#         }
#     return creds

#to connect with cloud sql deployed ---------------------------------------
from google.cloud.sql.connector import Connector
import sqlalchemy
from psycopg2.extras import RealDictCursor

# Your Cloud SQL connection details
INSTANCE_CONNECTION_NAME = 'aiml-ho-arg:asia-south1:newdb-demo1234',
DB_USER = "postgres"
DB_PASS = "Strateena@check"
DB_NAME = "new_db"

# ---------- SQLAlchemy Engine ----------
def cred():
    connector = Connector()

    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",   # or "psycopg2" if you prefer
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
        )
        return conn

    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    return engine

# ---------- Raw psycopg2 Query ----------
def db_query(query):
    connector = Connector()
    conn = None
    try:
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "psycopg2",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            results = cur.fetchall()
        return results
    except Exception as e:
        print("Database query error:", e)
        return []
    finally:
        if conn:
            conn.close()

# ---------- User Check ----------
def user_check():
    users = db_query("SELECT first_name, last_name, username, email, password_hash FROM users")
    creds = {"usernames": {}}
    for user in users:
        full_name = f"{user['first_name']} {user['last_name']}".strip()
        creds["usernames"][user["username"]] = {
            "name": full_name,
            "email": user["email"],
            "password": user["password_hash"]  # bcrypt-hashed passwords expected
        }
    return creds
