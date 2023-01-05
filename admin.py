from database_creator import create_connection
from helper import int_input

def login_admin():
    pwd = input("Enter the password: ")
    if pwd == "admin@123":
        print("Logged in as Admin.")
        return True
    else:
        print("Access denied.")

def create_train():
    train_id = int_input("Enter train ID: ")
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
        print("A train with this ID exists, please edit\
            or delete it.")
    else:
        train_name = input("Enter the name of the train: ")
        date = input("Enter the date of the train in the specified format - YYYY-MM-DD: ")
        origin = input("Enter the origin station and/or code: ")
        destination = input("Enter the destination station and/or code: ")
        regular = int_input("Enter the number of regular seats: ")
        tatkal = int_input("Enter the number of tatkal seats: ")

        cursor.execute(
            f'INSERT INTO schedule VALUES \
                ("{train_name}", "{date}", "{train_id}", "{origin}", "{destination}", {regular}, {tatkal}, 0, 0);'
        )
        conn.commit()
        conn.close()
        print("Train details saved.")

def edit_delete():
    choice = int_input("Please choose what you want to do:\n1. Delete train details\n2. Edit train details\n> ")
    train_id = int_input("Enter the train ID that you want to work with: ")

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
        if choice == 1:
            conf = input("Are you sure you want to delete this train ID? Enter YES (all caps) to confirm\n> ")
            if conf == "YES":
                cursor.execute(f'DELETE FROM schedule WHERE TID = {train_id};')
                conn.commit()
                conn.close()
                print(f"Train ID {train_id} deleted!")
            else:
                print("Confirmation failed, train details not deleted.")
        elif choice == 2:
            conf = input("Are you sure you want to edit this train ID? Enter YES (all caps) to confirm\n> ")
            if conf == "YES":
                cursor.nextset()
                cursor.execute(
                    f'SELECT * FROM schedule WHERE TID = {train_id};'
                )
                dataset = cursor.fetchone()
                tnameold, tdateold, tidold, originold, destold, regold, tatold, reg2old, tat2old = dataset
                train_name = input("Enter the name of the train: ")
                date = input("Enter the date of the train in the specified format - YYYY-MM-DD: ")
                origin = input("Enter the origin station and/or code: ")
                destination = input("Enter the destination station and/or code: ")
                regular = int_input("Enter the number of regular seats: ")
                tatkal = int_input("Enter the number of tatkal seats: ")

                cursor.nextset()
                cursor.execute(f'DELETE FROM schedule WHERE TID = {train_id};')
                conn.commit()

                cursor.execute(
                    f'INSERT INTO schedule VALUES \
                        ("{train_name}", "{date}", "{train_id}", "{origin}", "{destination}", {regular}, {tatkal}, {reg2old}, {tat2old});'
                )
                conn.commit()
                conn.close()
                print(f"Train details for {train_id} edited.")
            else:
                print("Confirmation failed, please try again.")
    else:
        print("The train ID you are looking for does not exist. Please check the ID and try again.")