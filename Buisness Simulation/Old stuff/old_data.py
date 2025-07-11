


def create_new_database():

    # clear existing database for a clear, new game

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(script_dir, "mybuisnessdatabase.db")

    # show current directory, for debugging
    #print("Current working directory:", os.getcwd())
    
    # Check if the database exists and remove it if it exist
    if os.path.exists(db_file):
        print(" Database found. Deleting it...")
        os.remove(db_file)
        print(" It's gone.")
    else:
        print(" No database found. Fresh start.")

    conn = sqlite3.connect('mybuisnessdatabase.db')  # Creates a new database file
    
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

    # Creating staff table, with name surname, ID (that is primary key), monthly salary, dish expertise
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        salary INTEGER,
        visiting_hours TIME,
        stay_time TIME,
        money_spent INTEGER,
        expertise TEXT
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

    cursor.execute("""
    INSERT INTO expenses (name, amount) 
    VALUES (?, ?);
    """, ("maintenance", 500))

    conn.commit()# commit code to the SQL file

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
    
    cursor.execute("""
    INSERT INTO transactions (date, transaction_name, amount, action, budget_after) 
    VALUES (?, ?, ?, ?, ?);
    """, (str(today), "Lottery Win", current_money, "added", current_money))

    conn.commit()# commit code to the SQL file

    # Creating schedule table, with sfaff member name surname and working hours (8h shifts 6-14, 14-22) 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        monday_6to14 INTEGER,
        monday_14to22 INTEGER,
        Tuesday_6to14 INTEGER,
        Tuesday_14to22 INTEGER,
        Wednesday_6to14 INTEGER,
        Wednesday_14to22 INTEGER,
        Thursday_6to14 INTEGER,
        Thursday_14to22 INTEGER,
        Friday_6to14 INTEGER,
        Friday_14to22 INTEGER,
        Saturday_6to14 INTEGER,
        Saturday_14to22 INTEGER,
        Sunday_6to14 INTEGER,
        Sunday_14to22 INTEGER   
    )''')

    conn.commit()# commit code to the SQL file

    print("----")

    return conn, cursor


# before the game start, create database, and remove the old one
conn, cursor = create_new_database() # as well as create cursor and connection, exported outside of functions