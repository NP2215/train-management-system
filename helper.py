from database_creator import create_connection
from prettytable import PrettyTable

def int_input(text):
    while True:
        data = input(text)
        if data.strip().isdigit():
            return int(data)
        else:
            print("Wrong input, please try again.")

def get_choice(length):
    while True:
        choice = int_input("Enter your choice: ")
        if choice in range(1, length + 1):
            return choice
        else:
            pass

def check_booking_id():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT BOOKINGID FROM booking_ids;'
    )

    data = cursor.fetchall()
    if not data:
        return 1
    else:
        req = int(data[-1][0]) + 1
        return req

def check_valid_trainid(train_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT TID FROM schedule;'
    )

    rst = cursor.fetchall()

    cursor.nextset()
    resultset = []

    if rst:
        for i in rst:
            resultset.append(i[0])

    if train_id in resultset:
        return train_id
    else:
        print("The train ID you are looking for does not exist.")

def view_trains():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM schedule;'
    )

    rst = cursor.fetchall()

    if rst:
        x = PrettyTable()
        x.field_names = ['Train Name', 'Date', 'Train ID', 'Origin', 'Destination', 'Regular seats available', 'Tatkal seats available', 'Regular seats booked', 'Tatkal seats booked']
        dummy = []

        for i in rst:
            dummy.append(list(i))

        x.add_rows(dummy)
        print(x)

    else:
        print("No trains have been added as of now.")

def create_display_table(l):
    x = PrettyTable()
    x.field_names = l[0]

    x.add_rows(l[1:])
    
    return x