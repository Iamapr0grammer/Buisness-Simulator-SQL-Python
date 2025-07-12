import sqlite3, os, datetime
from datetime import date

## Python program that communicates with datbase, placed all SQL stuff here to keep the program transparency

# list of every possible dishes in the game
dish_full_list = ["pizza", "kebab", "hamburger", "falafel", "gyro", "hummus", "caviar", "duck", "spaghetti", "lasagna", 
"rice", "thali", "chicken", "paella", "escargots", "garlic soup", "buritto", "tacos", "sushi", "sashimi", "pho", 
"harees", "pad thai", "shakshouka", "koshary", "couscous", "shwarma", "sandwich"]


# variables

today = date.today()
current_money = 1000000  # my current money, starting at 1 milion


# functions for Database controll

# what tables do I need?
# cash over time, monthly regular expenses, staff chart

def next_day():
    global today
    today = today + datetime.timedelta(days=1) # move 1 day forward
    return today


def create_new_database():
    global cursor, conn # export cursor and connection outside the function for later use

    # clear existing database for a clear, new game

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, "mybusinessdatabase.db")

    # show current directory, for debugging
    #print("Current working directory:", os.getcwd())
    
    # Check if the database exists and remove it if it exist
    if os.path.exists(db_file):
        print(" Database found. Deleting it...")
        os.remove(db_file)
        print(" It's gone.")
    else:
        print(" No database found. Fresh start.")

    conn = sqlite3.connect('mybusinessdatabase.db')  # Creates a new database file
    
    # create a cursor, that will be used to execute SQL commands
    cursor = conn.cursor()

    # Creating clients table, name, surname, client ID (that is primary key), typical visiting hours, avarage stay time, avarage money spent, age, favourite dish
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        visiting_hours TIME,
        stay_time TIME,
        money_spent INTEGER,
        favourite_dish TEXT,
        age INTEGER
    )
    ''')

    conn.commit()# commit code to the SQL file

    # Creating staff table, with name surname, ID (that is primary key), monthly salary
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        salary INTEGER,
        vacation_days INTEGER,
        loyalty INTEGER,
        job_start TIME,
        last_vacation TIME,
        age INTEGER,
        prior_expirience INTEGER,
        number of reprimands INTEGER
    )
    ''')

    conn.commit()# commit code to the SQL file

    # Creating expenses table, with list of all regular monthly expenses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount INTEGER
    )''')

    conn.commit()# commit code to the SQL file

    # Add all expenses

    # rent
    cursor.execute("""
    INSERT INTO expenses (name, amount) 
    VALUES (?, ?);
    """, ("rent", 7000))

    # maintenance
    cursor.execute("""
    INSERT INTO expenses (name, amount) 
    VALUES (?, ?);
    """, ("maintenance", 500))

    conn.commit()# commit code to the SQL file

    # Create Candidates Table, potential for Hire
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        date TIME,
        expected_salary INTEGER,
        age INTEGER,
        expirience
    )''')

    conn.commit()# commit code to the SQL file
    
    # add the fist transaction, of the player winning a lottery

    # Creating transaction table, with list of all transactions and the current budget
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        transaction_name TEXT NOT NULL,
        amount INTEGER,
        action,
        budget_after INTEGER
    )''')

    conn.commit()# commit code to the SQL file
    
    # add the fist transaction, of the player winning a lottery
    cursor.execute("""
    INSERT INTO transactions (date, transaction_name, amount, action, budget_after) 
    VALUES (?, ?, ?, ?, ?);
    """, (str(today), "Lottery Win", current_money, "added", current_money))

    conn.commit()# commit code to the SQL file

    print("----")

    return conn, cursor


def hire_employee():
    pass

def next_month_change():
    cursor.execute("SELECT SUM(amount) FROM expenses") # get the amount of summed expenses and add it together
    expenses = cursor.fetchone()

    gains = 0 # temporary it will be 0, later, revenue will be added

    results = gains - expenses[0]

    return results

def get_candidates():
    cursor.execute("SELECT * FROM candidates") # get the amount of summed expenses and add it together
    candidates = cursor.fetchall()
    return candidates

def add_candidates(list):
    global cursor, conn # export cursor and connection outside the function for later use

    for candidate in list:
        cursor.execute("""
        INSERT INTO candidates (name, surname, date, expected_salary, age, expirience) 
        VALUES (?, ?, ?, ?, ?, ?);
        """, (candidate[0], candidate[1], str(today), candidate[3], candidate[2], candidate[4]))
            # Name          Surname         Date          Age         Salary       Expirience

        conn.commit()# commit code to the SQL file


def hire_employee(cid):
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (cid,)) # move the candidated from the candidates database to the staff database
    candidate = cursor.fetchone()

    cursor.execute("""
        INSERT INTO staff (name, surname, job_start, salary, age, prior_expirience) 
        VALUES (?, ?, ?, ?, ?, ?);
        """, (candidate[0], candidate[1], str(today), candidate[3], candidate[2], candidate[4]))
            # Name          Surname         Date          Age         Salary       Expirience

    conn.commit()# commit code to the SQL file


    print("WTF : ", candidate)   # or do something productive with it


def delete_candidate(cid): # delete the candidate from the candidates database
    pass



# before the game start, create database, and remove the old one
conn, cursor = create_new_database() # as well as create cursor and connection, exported outside of functions