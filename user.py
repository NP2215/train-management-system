import mysql.connector as mycon
from database_creator import create_connection
import random

from helper import *

def user_login():
    username = int_input("Enter your user ID: ")
    conn = create_connection()
    cursor = conn.cursor()
    query = 'SELECT UID FROM credentials;'
    cursor.execute(query)
    rst = cursor.fetchall()
    resultset = []

    for i in rst:
        resultset.append(i[0])

    cursor.nextset()

    valid = True

    if resultset:
        if username in resultset:
            valid = False
            cursor.execute(
                f'SELECT USERNAME, PASSWORD FROM credentials WHERE UID = {username};'
            )
            uid, pwd = cursor.fetchone()
            password = input("Enter password: ")
            if password == pwd:
                print(f"Logged in as {username} ({uid}).")
                return username
            else:
                print("Access denied: Wrong password.")
                return user_login()

    if valid:
        choice = input("User ID not found. Do you want to create a new account?\n> ")
        if choice.lower().strip() == 'yes':
            while True:
                while True:
                    while True:
                        username = input("Enter username: ")
                        cursor.nextset()
                        cursor.execute(
                            f'SELECT * FROM credentials WHERE USERNAME = "{username}";'
                        )
                        dataset = cursor.fetchall()
                        if not dataset:
                            break
                        else:
                            print("This username is already taken, please enter another username.")
                    user_re = input("Enter username again: ")
                    if username == user_re:
                        break
                    else:
                        print("Usernames do not match, please try again. ")
                pwd = input("Enter password: ")
                pwd_re = input("Enter password again: ")
                
                if pwd == pwd_re and username == user_re:
                    cursor.execute(
                        'SELECT UID FROM credentials;'
                    )
                    testset1 = cursor.fetchall()
                    cursor.nextset()
                    used_ids = [x[0] for x in testset1]

                    while True:
                        newid = random.randint(10000, 99999)
                        if newid not in used_ids:
                            break

                    cursor.execute(
                        f'INSERT INTO credentials VALUES ({newid}, "{username}", "{pwd}")'
                    )
                    print(f"User created with user id {newid}, please login again.")
                    conn.commit()
                    conn.close()
                    return user_login()
                else:
                    print("Passwords don't match. Please try again.")

def create_booking(username):
    view_trains()
    train_id = int_input("Enter the train ID of the train you wish to book: ")
    
    check = check_valid_trainid(train_id)

    conn = create_connection()
    cursor = conn.cursor()

    if check:
        cursor.execute(
            f'SELECT * FROM schedule WHERE TID = {train_id};'
        )
        train_name, train_date, tid, origin, dest, reg1, tat1, reg2, tat2 = cursor.fetchone()
        nop = int_input("Enter the number of passengers that you wish to create the booking for: ")
        while True:
            booking_type = int_input("Please choose your type of booking\n1. Regular\n2. Tatkal\n> ")
            if booking_type in [1, 2]:
                break
            else:
                print("Wrong input, try again.")
        if booking_type == 1:
            if reg2 + nop > reg1:
                print("Sorry, insufficient seats.")
                return
            else:
                reg2 += nop
                btype = 'REGULAR'

        elif booking_type == 2:
            if tat2 + nop > tat1:
                print("Sorry, insufficient seats.")
                return
            else:
                btype = 'TATKAL'
                tat2 += nop

        bid = check_booking_id()

        dummy = [["Booking ID", "Name", "Age", "Origin", "Destination", "Train ID", "Date of Travel"]]
        d2 = []
        for i in range(nop):
            name, age = input("Enter passenger name: "), int_input("Enter passenger age: ")
            dummy.append([bid, name, age, origin, dest, train_id, train_date])
            d2.append((name, age, train_id, bid, btype))

        print(create_display_table(dummy))

        conf = input("Do you want to confirm this booking? Enter YES (all caps)\n> ")

        if conf == "YES":
            cursor.nextset()
            cursor.execute(
                f'INSERT INTO booking_ids VALUES ({bid}, {username}, {train_id})'
            )
            conn.commit()

            cursor.nextset()
            cursor.execute(
                f'UPDATE schedule SET REG_BOOKED = {reg2}, TATKAL_BOOKED = {tat2} WHERE TID = {train_id};'
            )
            conn.commit()

            for i in d2:
                cursor.nextset()
                pname, page, tid, bid, btype = i
                cursor.execute(
                    f'INSERT INTO bookings VALUES ("{pname}", {int(page)}, {int(tid)}, {int(bid)}, "{btype}");'
                )
                conn.commit()
            conn.close()

            print("Booking saved.")
        else:
            print("Cancelled.")

def view_bookings(user_id, valid = None):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        f'SELECT BOOKINGID FROM booking_ids WHERE UID = {user_id};'
    )

    dummy = [["Train ID", "Booking ID", "Number of passengers"]]
    rst = cursor.fetchall()
    cursor.nextset()

    dataset = [i[0] for i in rst]

    for i in dataset:
        cursor.execute(
            f'SELECT COUNT(*) FROM bookings WHERE BOOKINGID = {i};'
        )

        nop = cursor.fetchone()[0]
        cursor.nextset()

        cursor.execute(
            f'SELECT TID FROM bookings WHERE BOOKINGID = {i};'
        )

        train_id = cursor.fetchone()[0]
        cursor.nextset()
        
        dummy.append([f"{train_id}", f"{i}", f"{nop}"])

    print(create_display_table(dummy))

    cursor.nextset()
    if valid:
        bid = int_input("Enter the booking ID you wish to view: ")
        if bid in dataset:
            cursor.execute(
                f'SELECT * FROM bookings WHERE BOOKINGID = {bid}'
            )
            dataset = cursor.fetchall()

            dummy = [["Passenger Name", "Passenger age", "Train ID", "Booking ID", "Booking Type"]]

            for i in dataset:
                dummy.append(list(i))

            print(create_display_table(dummy))
    
    conn.close()
    return dataset

def edit_bookings(user_id):
    dataset = view_bookings(user_id)

    conn = create_connection()
    cursor = conn.cursor()

    bid = int_input("Enter the booking ID you wish to edit: ")
    if bid in dataset:
        cursor.execute(
            f'SELECT * FROM bookings WHERE BOOKINGID = {bid}'
        )
        dataset = cursor.fetchall()

        cursor.nextset()
        for i in dataset:
            pname, page, tid, bid, btype = i
            print(f"Passenger details:\nPassenger name: {pname}\nPassenger age: {page}")
            conf = input("Do you want to edit the details for this passenger? [Y/N]: ")
            if conf.lower().strip() == 'y':
                pnamen, pagen = input("Enter passenger name: "), int_input("Enter passenger age: ")
                cursor.execute(
                    f'DELETE FROM bookings \
                        WHERE PNAME = "{pname}" AND PAGE = {page} AND BOOKINGID = {bid};'
                )
                conn.commit()
                cursor.execute(
                    f'INSERT INTO bookings VALUES ("{pnamen}", {pagen}, {tid}, {bid}, "{btype}");'
                )
                conn.commit()
            print("Passenger details updated!")

        
    else:
        print("The booking ID you are looking for does not exist.")

def delete_booking(user_id):
    dataset = view_bookings(user_id)

    conn = create_connection()
    cursor = conn.cursor()

    bid = int_input("Enter the booking ID you wish to delete: ")

    if bid in dataset:
        cursor.execute(
            f'SELECT * FROM bookings WHERE BOOKINGID = {bid}'
        )
        dataset = cursor.fetchall()
        cursor.nextset()

        nop = len(dataset)

        dummy = [["Passenger Name", "Passenger age", "Train ID", "Booking ID", "Booking Type"]]

        for i in dataset:
            pname, page, tid, bid, btype = i
            dummy.append(list(i))

        if btype == "REGULAR":
            cursor.execute(
                f'UPDATE schedule SET REG_BOOKED = REG_BOOKED - {nop} WHERE TID = {tid};'
            )
        else:
            cursor.execute(
                f'UPDATE schedule SET TATKAL_BOOKED = TATKAL_BOOKED - {nop} WHERE TID = {tid};'
            )
        conn.commit()

        print(create_display_table(dummy))

        cursor.nextset()

        conf = input("Are you sure you want to delete this booking? Enter YES (all caps)\n> ")
        if conf == "YES":
            cursor.execute(
                f'DELETE FROM booking_ids WHERE BOOKINGID = {bid}'
            )
            conn.commit()
            conn.close()
            print("Deleted this booking.")
        else:
            print("Cancelled")
    else:
        print("Wrong booking ID, please try again.")