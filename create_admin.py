import os
import psycopg2

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


load_dotenv()


username = input("Enter admin username: ")
password = input("Enter admin password: ")

password_hash = generate_password_hash(password)


conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)


cur = conn.cursor()


cur.execute(
    """
    INSERT INTO users (username, password)
    VALUES (%s, %s)
    """,
    (username, password_hash)
)


conn.commit()

cur.close()
conn.close()

print("Admin account created successfully!")