from admin import *
from user import *
from helper import *

from database_creator import *

initialise_database()

menus = [
    'Please choose your mode of login:\n1. Admin\n2. User',
    'Please choose what you want to do:\n1. View trains\n2. Create a new booking\n3. Edit a booking\n4. Delete a booking\n5. View your bookings\n6. Logout',
    'Please choose what you want to do:\n1. Add new train\n2. Edit or delete a train\n3. View trains\n4. Logout'
]


admin_log, logged_in = False, False
valid = False

while not valid:
    print(menus[0])
    choice = get_choice(2)
    if choice == 1:
        admin_log = login_admin()
        if admin_log:
            valid = True
        else:
            print("Wrong login, please try again.")
    else:
        logged_in = user_login()
        if user_login:
            valid = True
        else:
            print("Wrong login, please try again.")

while True:
    if logged_in:
        print(menus[1])
        choice = get_choice(6)
        if choice == 1:
            view_trains()
        elif choice == 2:
            create_booking(logged_in)
        elif choice == 3:
            edit_bookings(logged_in)
        elif choice == 4:
            delete_booking(logged_in)
        elif choice == 5:
            view_bookings(logged_in, True)
        elif choice == 6:
            print("Thank you!")
            exit()


    elif admin_log:
        print(menus[2])
        choice = get_choice(4)
        if choice == 1:
            create_train()
        elif choice == 2:
            edit_delete()
        elif choice == 3:
            view_trains()
        elif choice == 4:
            print("Thank you!")
            exit()