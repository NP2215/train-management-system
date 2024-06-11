# About the Project

A Python and MySQL connected project that works as a train management system. Provides admin accounts, which is used to schedule trains. Provides the possibility to create multiple user accounts with user names, user IDs and passwords to create reservations in the created trains.

# Requirements

The project is dependent on MySQL, and hence requires a connector. The other main modules used in this project include prettytable, used to display the data.
Python versions of 3.8 and higher and preferred for this project.

# Description of files

- **main.py**: 
This file consists of all the main functions of the file. This is the file that must be run in order to execute the project.

- **user.py**: 
This file consists of all the functions that are available to the user. Dependent on `helper.py` and `database_creator.py`.

- **admin.py**: 
This file consists of all the functions that are available to the admin. Dependent on `helper.py` and `database_creator.py`.

- **helper.py**: 
Consists of helper functions.

- **database_creator.py**: 
Consiss of the functions that are related to the creation and manipulation of the database structure.

# How to run the project

1. Download the entire project, then create a virtual environment:
```
python -m venv env
```

2. Activate the environment:
- For Windows (Win)
```
env\Scripts\activate
```
- For Macintosh (DarWin)
```
source env/bin/activate
```

3. Download all packages:
```
pip install -r requirements.txt
```

4. Run the `main.py` file:
```
python main.py
```

# Areas to improve

- The project can further be added with a GUI (for example a web interface with `Django`) to enhance user experience.
- It can also be used with fares to create a full fledged train management system.
