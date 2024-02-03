import psycopg2

# Database connection parameters
dbname = 'stores'
user = 'jerrylin'
## No password
# password = 'your_password'
host = 'localhost'

# Connect to postgres DB
conn = psycopg2.connect(dbname=dbname, user=user, host=host)


# Open a cursor to perform database operations
cur = conn.cursor()

# Close the cursor & connection
cur.close()
conn.close()
