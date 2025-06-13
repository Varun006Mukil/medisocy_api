# import os
# import pymysql  # or your driver


# def get_connection():
# 	return pymysql.connect(
#     host=os.getenv("DB_HOST"),
#     # port=int(os.getenv("DB_PORT", 3306)),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )

from settings import Settings
import pymysql

settings = Settings()

def get_connection():
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )