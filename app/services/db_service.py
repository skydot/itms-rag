import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "trms_user"),
        password=os.getenv("DB_PASSWORD", "trms123"),
        database=os.getenv("DB_NAME", "trms_dump"),
        cursorclass=pymysql.cursors.DictCursor
    )
