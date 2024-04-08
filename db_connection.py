import os
import mysql.connector
from dotenv import load_dotenv, dotenv_values 

# loading variables from .env file
load_dotenv()


conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USERNAME"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DBNAME")
)

cursor = conn.cursor()