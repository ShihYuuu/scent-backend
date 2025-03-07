# import mysql.connector
import os
from dotenv import load_dotenv
import pymysql

# 加載環境變數
load_dotenv()

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            user=os.getenv("MYSQL_USER", "root"),
            # password=os.getenv("MYSQL_PASSWORD", ""), # 目前沒有密碼
            database=os.getenv("MYSQL_DB", "testdb"),
            cursorclass=pymysql.cursors.DictCursor 
        )
        print("DB connect success!!!")
        return connection
    except pymysql.MySQLError as e:
        print(f"DB connect fail: {e}")
        return None
    
    # connection = mysql.connector.connect(
    #     host=os.getenv("MYSQL_HOST"),
    #     user=os.getenv("MYSQL_USER"),
    #     password=os.getenv("MYSQL_PASSWORD"),
    #     database=os.getenv("MYSQL_DB"),
    # )