import psycopg2
import json

# Database connection parameters
dbname = 'stores'
user = 'jerrylin'
host = 'localhost'

# Function to connect to the database
def get_db_connection():
    conn = psycopg2.connect(dbname=dbname, user=user, host=host)
    return conn

# Function to insert JSON data
def insert_json_data(json_data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO json_data (data) VALUES (%s)", [json.dumps(json_data)])
    conn.commit()
    cur.close()
    conn.close()

# Function to update JSON data
def update_json_data(id, json_data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE json_data SET data = %s WHERE id = %s", [json.dumps(json_data), id])
    conn.commit()
    cur.close()
    conn.close()