import mysql.connector
import os

# Database Connection Setup
def get_db():
    mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    return mydb

def reconnect_to_db(mydb):
    try:
        # Attempt to connect to our database.
        mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

        # Check if our tables exist.
        cursor = mydb.cursor()
        cursor.execute(f"USE {os.getenv('DB_NAME')}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if not tables:
            init_db(mydb)
        cursor.close()
        print("Connected to database!")

    # But if anything were to go very wrong...
    except mysql.connector.Error as err:
        if err.errno == 1049:  # This is the error code for "Unknown database", so let's try recreating it!
            init_db(mydb)
        else:
            # If you end up here, you should be very frustrated.
            print(f"Error connecting to database: {err}")
            mydb.disconnect()
            exit(1)

# Initialize the database from the schema in init.sql, in the case it doesn't exist.
def init_db(mydb):
    print("Attempting to recreate database from schema in init.sql...")
    try:
        cursor = mydb.cursor()
        with open('init.sql', 'r') as file:
            sql_script = file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        mydb.commit()
        # If you end up here, you should be very happy.
        print("Database initialized successfully!")
        cursor.close()
    except mysql.connector.Error as err:
        # If you end up here, you should be very confused.
        print(f"Error recreating database: {err}")
        print("THIS MIGHT CAUSE WEIRD THINGS TO HAPPEN IF YOU DON'T FIX IT!!")
        if cursor:
            cursor.close()
