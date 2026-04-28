# db.py
# This file gives every other module a connection to MySQL.
# Just call get_connection() and you're ready to run queries.
 
import mysql.connector
from config import DB_CONFIG
 
 
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)