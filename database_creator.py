import mysql.connector as mycon

def create_connection():
    conn = mycon.connect(
        username = "root",
        password = "Welcome123$",
        host = "localhost",
        database = "trains_db"
    )

    return conn


def initialise_database():
    conn = mycon.connect(
        username = "root",
        password = "Welcome123$",
        host = "localhost"
    )

    queries = [
        "CREATE DATABASE IF NOT EXISTS trains_db;",
        "USE trains_db;",
        "CREATE TABLE IF NOT EXISTS credentials(\
            UID INT PRIMARY KEY,\
            USERNAME VARCHAR(30) UNIQUE NOT NULL,\
            PASSWORD VARCHAR(15)\
            );",
        "CREATE TABLE IF NOT EXISTS schedule(\
            TNAME VARCHAR(45),\
            TDATE DATE,\
            TID INT PRIMARY KEY,\
            ORIGIN VARCHAR(20),\
            DESTINATION VARCHAR(20),\
            REGULAR INT,\
            TATKAL INT,\
            REG_BOOKED INT,\
            TATKAL_BOOKED INT\
            );",
        "CREATE TABLE IF NOT EXISTS booking_ids(\
            BOOKINGID INT PRIMARY KEY,\
            UID INT,\
            TID INT,\
            FOREIGN KEY (UID) REFERENCES credentials(UID) ON DELETE CASCADE,\
            FOREIGN KEY (TID) REFERENCES schedule(TID) ON DELETE CASCADE\
            );",
        "CREATE TABLE IF NOT EXISTS bookings(\
            PNAME VARCHAR(45),\
            PAGE INT,\
            TID INT,\
            BOOKINGID INT,\
            BTYPE VARCHAR(10),\
            FOREIGN KEY (TID) REFERENCES schedule(TID) ON DELETE CASCADE,\
            FOREIGN KEY (BOOKINGID) REFERENCES booking_ids(BOOKINGID) ON DELETE CASCADE\
            );"
    ]

    cursor = conn.cursor()

    for i in queries:
        cursor.execute(i)
        conn.commit()

    cursor.close()
    conn.close()

    print("Database initialised!")