
# IMPORT EVERYTHING HERE!

import sqlite3
import time, random, os, datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# set up global variables, that will be used in the program below


today = date.today()

current_money = 1000000  # my current money, starting at 1 milion


# list of every possible dishes in the game
dish_full_list = ["pizza", "kebab", "hamburger", "falafel", "gyro", "hummus", "caviar", "duck", "spaghetti", "lasagna", 
"rice", "thali", "chicken", "paella", "escargots", "garlic soup", "buritto", "tacos", "sushi", "sashimi", "pho", 
"harees", "pad thai", "shakshouka", "koshary", "couscous", "shwarma", "sandwich"]

print("Number of dishes: ", len(dish_full_list))


# list of male names
male_names = [
    # Standard Male Names
    "Adam", "Ben", "Carl", "David", "Ethan", "Frank", "George", "Henry",
    "Ian", "Jack", "Kyle", "Luke", "Mark", "Nathan", "Oliver", "Paul",
    "Quentin", "Ryan", "Steve", "Tom", "Victor", "William", "Xavier", "Yanni", "Zach",
    
    # Nerd-Approved Names
    "Alan", "Dennis", "Guido", "Linus", "Elon", "Bill", "Steve",
    "Richard", "Tim", "Bjarne",
    
    # version 2
    "Greg", "Todd", "Chuck", "Barry",
    "Neil", "Phil", "Craig",
    "Randy", "Doug", "Frank",
    
    # Overkill Names
    "Maximus", "Thorvald", "Magnus", "Apollo", "Xerxes", "Leonardo",
    "Hannibal", "Atticus", "Titan", "Zephyr"
]

# list of female names
female_names = [
    # Standard Female Names
    "Alice", "Beth", "Clara", "Diana", "Emma", "Fiona", "Grace", "Hannah",
    "Isla", "Jane", "Katie", "Luna", "Maria", "Nina", "Olivia", "Penny",
    "Queenie", "Rachel", "Sarah", "Tina", "Uma", "Vera", "Wendy", "Xena", "Yara", "Zoe",
    
    # Nerd-Approved Names
    "Ada",       
    "Grace",     
    "Radia",     
    "Margaret",  
    "Joan",      
    "Barbara",   
    "Karen",    
    "Frances",  
    "Marissa",   
    "Shafi",     

    # version 2
    "Sally", "Tina", "Claire", "Bonnie",
    "Nina", "Faye", "Cassie",
    "Rita", "Deb", "Wanda",

    # Overkill Names
    "Athena", "Freya", "Seraphina", "Bellatrix", "Juno", "Andromeda",
    "Lilith", "Electra", "Valkyrie", "Nova"
]


# list of family names
family_names = [
    # Common and Classic
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",

    # Nerd-Approved Surnames
    "Turing",       
    "Hopper",       
    "Lovelace",     
    "Hamilton",     
    "Knuth",        
    "Liskov",       
    "Torvalds",     
    "Dijkstra",     
    "Berners-Lee",  
    "Spärck Jones", 

    # Fictionally Spicy
    "Skywalker", "Kenobi", "Stark", "Wayne", "Potter", "Malfoy", "Snape",
    "Romanoff", "Banner", "Holmes", "Moriarty", "Riker", "Picard", "Ripley", "Kirk",

    # Unnecessarily Cool
    "Ravenwood", "Storm", "Blackthorn", "Graves", "Nightshade", "Blaze",
    "Ashcroft", "Thorne", "Hawke", "Crimson"
]

# all windows that will be used in this game, and all charts will be assigned to a seperate window
windows = {}



# ==================================    DEFINE ALL FUNCTIONS    ====================================================

# Create windows charts that will be used in this program

#def create_chart_window(name, data_x, data_y, title):

def create_specific_chart(name, title, win):
    
    # Create the test matplotlib chart
    fig, ax = plt.subplots(figsize=(4, 2))

    #ax.plot([1, 2, 3, 4], [random.randint(10, 100) for _ in range(4)])  # dummy data

    # replace dummy data with real data, also sort them by date, ASC = ascending
    cursor.execute("SELECT * FROM transactions ORDER BY date ASC")

    # format: date, transaction_name, amount, action, budget_after
    rows = cursor.fetchall()

    dates = []
    money = []

    for i in rows:
        dates.append(datetime.datetime.strptime(i[1], "%Y-%m-%d"))
        money.append(i[5])

    ax.plot(dates, money, marker='o', linestyle='-')  # Add dots for clarity

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Budget ($)")  # Or whatever currency you're rich in 😂

    # Rotate dates so they don't overlap
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Tight layout so labels don't get cut off
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return fig


def next_day():
    global today
    today = today + datetime.timedelta(days=1) # move 1 day forward
    return today


def create_chart_window(name, title):
    
    if name in windows:
        print(name, " this window already exists, ignore the command")
        return  # Already created, ignore it
    else:
        print(name, " this window does not exist, we will create it right now")

    # Create a separate window for this chart
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x300")
    #win.withdraw()  # Hide it at first

    # Create the chart and return it, so that it can be closed later
    new_chart = create_specific_chart(name, title, win)

    # override the default WM_DELETE_WINDOW behavior to remove it from your windows dict before it gets destroyed
    def on_close():
        print(f"{name} window closed.")
        windows.pop(name, None)
        plt.close(new_chart) # close the chart
        win.destroy()
    
    win.protocol("WM_DELETE_WINDOW", on_close)

    windows[name] = win


def create_money_chart():
    create_chart_window("Money Chart", "Budget Over Time")


def remove_money(amount, reason):
    global cursor, conn
    money_before = get_current_money()
    money_after = money_before - amount
    cursor.execute("""
    INSERT INTO transactions (date, transaction_name, amount, action, budget_after) 
    VALUES (?, ?, ?, ?, ?);
    """, (str(today), str(reason), amount, "removed", money_after))
    conn.commit()

def get_current_money():
    global cursor, conn
    cursor.execute("SELECT budget_after FROM transactions ORDER BY id DESC LIMIT 1;")
    result = cursor.fetchone()
    return result[0]


def add_money(amount, reason):
    global cursor, conn
    money_before = get_current_money()
    money_after = money_before + amount
    cursor.execute("""
    INSERT INTO transactions (date, transaction_name, amount, action, budget_after) 
    VALUES (?, ?, ?, ?, ?);
    """, (str(today), str(reason), amount, "added", money_after))
    conn.commit()


def generate_person():
    sex = random.randint(1,2)
    if sex == 1:
        sex = "male"
    else:
        sex = "female"
    
    name = ""

    if sex == "male":
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    family_name = random.choice(family_names)

    age = random.randint(18,100)

    dish = random.choice(dish_full_list)

    person = [name, family_name, dish, age, sex]

    return person


def new_customer():
    pass


# simulate the single day, with customers, revenue, etc
def simulate_single_day():

    # Customers
    cursor.execute("SELECT * FROM clients") # get all customers in a list

    # format: date, transaction_name, amount, action, budget_after
    customers = cursor.fetchall()

    print(generate_person())



# a whole month, consisting of around 30 days
def simulate_a_whole_month():
    global today
    old_month = today.strftime("%B")

    # simulate days as long as the month is the same
    while old_month == today.strftime("%B"):
        # print(f" Today day is: {today.strftime("%A")}, | and: {today}") # for testing if needed
        simulate_single_day() # do whatever you have to do this day
        today = next_day() # move on to the next day




# this function is called, then the user clicks the next month button.
def next_month():
    global cursor, conn, today

    print("📅 Moving to the next month...")
    simulate_a_whole_month()

    # what should happen at the end of the month?

    # emplyees get their Salary

    # espenses are paid

    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()

    remove_money(result[0], "regular monthly expenses")

    # more_money = random.randint(3750, 11250)

    # add_money(more_money, "random money add")

    print("----")

    # every day of the month is simulated, with clients, purchases, etc

    display_money = get_current_money()

    money_label.config(text=f"Your Current Budget: {display_money}")
    print(f"💸 Spent: {result[0]} | Remaining: {display_money}")

    predicted_change = predict_next_month_change()

    expected_money_change_label.config(text=f"Expected money next month: {predicted_change}")

    # change color based on espected change
    if predicted_change < 0:
        expected_money_change_label.config(fg="red")
    else:
        expected_money_change_label.config(fg="green")
        
        

    


# function to Show window when needed
def show_chart_window(name):
    if name in windows:
        windows[name].deiconify()  # Show window
        windows[name].lift()       # Bring to front



# function that will predict the change of money, based on expected expenses
def predict_next_month_change():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    expenses = cursor.fetchone()

    gains = 0

    results = gains - expenses[0]

    return results



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





# =====================================================    Main Game Window   ======================================



# before the game start, create database, and remove the old one
conn, cursor = create_new_database() # as well as create cursor and connection, exported outside of functions

#print(conn, cursor) # test if they are created

# main game window
root = tk.Tk()
root.title("MyBuisness By Maciej Wątor") 


# AFTER "root" is created -> create all necessary charts, user will just hide/reveal them
# create_chart_window("Money Chart", "Budget Over Time")

# Display the current money, that the user has at their disposal
money_label = tk.Label(root, text=f"Your Current Budget: {current_money}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
money_label.pack(pady=10)

# Display the expected change for the next month
expected_money_change_label = tk.Label(root, text=f"Expected money next month: {predict_next_month_change()}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
expected_money_change_label.pack(pady=10)

# set the window size and color
root.geometry("500x500")
root.config(bg="#2d2d2d")  # Dark theme because we're edgy

# button to progress the game to next month
money_chart_btn = tk.Button(root, text="Show Money Chart!", command=create_money_chart, bg="#aa0000", fg="white")
money_chart_btn.pack(pady=10)


# button to progress the game to the next month
game_start_btn = tk.Button(root, text="Next Month!", command=next_month, bg="#aa0000", fg="white")
game_start_btn.pack(pady=10)


root.mainloop()

print("PROGRAM END")