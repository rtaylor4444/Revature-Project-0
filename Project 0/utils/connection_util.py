from psycopg2 import connect
from psycopg2._psycopg import OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_TYPE'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            port=os.environ.get('DB_PORT')
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
