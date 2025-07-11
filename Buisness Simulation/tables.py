from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import data, generator


## co dalej?
# Podłączenie tego do Database

# job posting:
job_post_active = False
salary_offer = 0

# sample data:
currest_staff = 50 # the amount of staff currently working
hiring_status = "Now Hiring"
expected_money_change = data.next_month_change()
money = 1000000

# === CHART FUNCTIONS ===

def create_money_chart():
    global money_chart
    print("create Money Chart")

    # Create subwindow
    money_chart = tk.Toplevel()
    money_chart.title("Money Chart")
    money_chart.geometry("400x400+350+50")
    money_chart.config(bg="#2d2d2d")

    # Sample Data
    days = [1, 2, 3, 4, 5, 6, 7]
    money = [1000, 1200, 1100, 1300, 1250, 1400, 1350]

    # Create figure
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.plot(days, money, color="lime", marker='o')
    ax.set_title("Cash Over Time", color="white")
    ax.set_xlabel("Day", color="white")
    ax.set_ylabel("PLN", color="white")
    ax.set_facecolor("#2d2d2d")
    fig.patch.set_facecolor('#2d2d2d')
    ax.tick_params(colors='white')

    # Embed plot in tkinter
    canvas = FigureCanvasTkAgg(fig, master=money_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # overrite close button
    def money_chart_close():
        money_chart.withdraw()

    # override the close button to kill the app
    money_chart.protocol("WM_DELETE_WINDOW", money_chart_close)


def create_expenses_chart():
    global expenses_chart
    print("create Expenses Chart")

    expenses_chart = tk.Toplevel()
    expenses_chart.title("Expenses Chart")
    expenses_chart.geometry("400x400+780+50")
    expenses_chart.config(bg="#2d2d2d")


    # Sample Data
    labels = ['Food', 'Salaries', 'Marketing', 'Maintenance']
    sizes = [300, 700, 150, 100]

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color':"white"}
    )
    ax.set_title("Expense Breakdown", color="white")
    fig.patch.set_facecolor('#2d2d2d')
    ax.set_facecolor("#2d2d2d")

    canvas = FigureCanvasTkAgg(fig, master=expenses_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # overrite close button
    def expenses_chart_close():
        expenses_chart.withdraw()

    # override the close button to kill the app
    expenses_chart.protocol("WM_DELETE_WINDOW", expenses_chart_close)


def create_staff_chart():
    global staff_chart
    print("create Staff Chart")

    staff_chart = tk.Toplevel()
    staff_chart.title("Staff Chart")
    staff_chart.geometry("400x400+350+500")
    staff_chart.config(bg="#2d2d2d")

    # Sample Data
    statuses = ['Working', 'On Vacation', 'Training', 'Sick']
    counts = [5, 2, 1, 1]

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    bars = ax.bar(statuses, counts, color='skyblue')
    ax.set_title("Staff Status", color="white")
    ax.set_ylabel("Number of Staff", color="white")
    ax.set_facecolor("#2d2d2d")
    fig.patch.set_facecolor('#2d2d2d')
    ax.tick_params(colors='white')

    canvas = FigureCanvasTkAgg(fig, master=staff_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # overrite close button
    def staff_chart_close():
        staff_chart.withdraw()

    # override the close button to kill the app
    staff_chart.protocol("WM_DELETE_WINDOW", staff_chart_close)



hired_ids = set()   # store hired candidate IDs, replace that later


# ── Window factory ────────────────────────────────────────────────────────
def create_hire_window():
    global hire_window, tree

    hire_window = tk.Toplevel()
    hire_window.title("Candidate List")
    hire_window.geometry("600x400+780+510")
    hire_window.config(bg="#2d2d2d")

    # ── Treeview + scrollbar frame ───────────────────────────────────────
    frame = tk.Frame(hire_window, bg="#2d2d2d")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ("name", "exp", "salary")
    tree = ttk.Treeview(
        frame, columns=columns, show="headings",
        yscrollcommand=scrollbar.set, selectmode="browse"
    )
    scrollbar.config(command=tree.yview)

    # Headings
    tree.heading("name",   text="Name")
    tree.heading("exp",   text="Expirience")
    tree.heading("salary", text="Expected Salary")

    # Column widths / alignment
    tree.column("name",   width=180)
    tree.column("exp",   width=220)
    tree.column("salary", width=120, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    def add_candidate(cand):
        print(cand)
        # text_salary = f"{cand[4]} PLN"
        # hire_window.tree.insert("", tk.END, iid=cand["id"],
        #             values=(cand["name"], cand["qual"], text_salary))

    # ── Action buttons (Hire / Reject) ───────────────────────────────────
    btn_frame = tk.Frame(hire_window, bg="#2d2d2d")
    btn_frame.pack(pady=10)

    def hire_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        hired_ids.add(cid)
        tree.delete(cid)
        messagebox.showinfo("Hired!", f"Candidate {cid} joins the payroll.\nYour problem now.")

    def reject_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        tree.delete(cid)
        messagebox.showinfo("Rejected", f"Candidate {cid} escorted off the premises.")

    hire_btn   = tk.Button(btn_frame, text="Hire",   width=12, bg="#008f39", fg="white",
                           command=hire_selected)
    reject_btn = tk.Button(btn_frame, text="Reject", width=12, bg="#cc0000", fg="white",
                           command=reject_selected)
    hire_btn.grid(row=0, column=0, padx=10)
    reject_btn.grid(row=0, column=1, padx=10)

    # overrite close button
    def hire_window_close():
        hire_window.withdraw()

    # override the close button to kill the app
    hire_window.protocol("WM_DELETE_WINDOW", hire_window_close)



def create_job_offer_window():
    global job_offer

    print("create Staff Chart")

    job_offer = tk.Toplevel()
    job_offer.title("Candidates for hire")
    job_offer.geometry("300x200+1200+50")
    job_offer.config(bg="#2d2d2d")

    # Salary Label
    label = tk.Label(job_offer, text="Choose Salary Offer:", fg="white", bg="#2d2d2d", font=("Helvetica", 12))
    label.pack(pady=(20, 5))

    # Dropdown for salary options
    salary_options = [3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000]
    selected_salary = tk.StringVar()
    salary_dropdown = ttk.Combobox(job_offer, textvariable=selected_salary, values=salary_options, state="readonly")
    salary_dropdown.current(0)  # Default selection
    salary_dropdown.pack(pady=5)

    # Label
    quide_label = tk.Label(job_offer, text="Industry Salary Standard: 4500 PLN", fg="white", bg="#2d2d2d", font=("Helvetica", 12))
    quide_label.pack(pady=(20, 5))

    # Post button
    def post_offer():
        global job_post_active, salary_offer
        chosen = selected_salary.get()
        job_post_active = True
        stop_hire_window_btn.place(x=10, y=260)

        salary_offer = int(chosen)

        print(f"Posted job offer with salary: {chosen}")
        # You can store this choice somewhere or trigger actual logic here

    post_button = tk.Button(job_offer, text="Post Job Offer", command=post_offer, bg="#aa0000", fg="white")
    post_button.pack(pady=20)

    # overrite close button
    def job_offer_close():
        job_offer.withdraw()

    # override the close button to kill the app
    job_offer.protocol("WM_DELETE_WINDOW", job_offer_close)



def update_display():
    global root, money
    expected_money_change = data.next_month_change()
    money = money + expected_money_change
    money_label.config(text=f"Your Budget: {money}")
    expected_money_change_label.config(text=f"Estimated turnover: {expected_money_change}")

    # change color based on espected change
    if expected_money_change < 0:
        expected_money_change_label.config(fg="red")
    else:
        expected_money_change_label.config(fg="green")
    
    # update the date
    today_label.config(text=f"Today: {data.today}")





# show charts functions

def show_money_chart():
    money_chart.deiconify()
    

def show_expenses_chart():
    expenses_chart.deiconify()
    

def show_staff_chart():
    staff_chart.deiconify()


# show window functions

def show_hire_window():
    job_offer.deiconify()

def show_candidates_window():
    hire_window.deiconify()

def show_candidates_button():
    pass

def hide_candidates_button():
    pass

# a button to hide/reveal all windows with just one click
def hide_all():
    pass

# === MAIN WINDOW ===

def next_month():
    update_all_charts()
    update_display()
    print(data.next_day())

    # generate all events
    if job_post_active:
        candidates = generator.chance_for_new_candidate(salary_offer) # generates new candidates and places them inside the database
        data.add_candidates(candidates)
        print(candidates)


def stop_hiring():
    global job_post_active
    #candidates_btn.place(x=100, y=260)
    stop_hire_window_btn.place_forget()

    # job posting:
    job_post_active = False

def update_candidates():
    """Pull new candidates from DB (or dummy list) and refresh the tree."""
    if tree is None:   # window not created yet
        return

    # 1) fetch fresh candidates ------------------------------------------------
    candidates = data.get_candidates()   # expects list of tuples / dicts
    # dummy fallback:
    # rows = [(1,"Jan","Chef 3y",3500), (2,"Anna","Waitress",2900)]

    # 2) clear current table -------------------------------------------
    tree.delete(*tree.get_children())

    # 3) insert rows ----------------------------------------------------
    for cand in candidates:
        # adapt to your real tuple / dict shape:

        print(cand)
        full_name = str(cand[1] + cand[2])
        id = cand[0]

        tree.insert("", tk.END, iid=id,
                    values=(full_name, f"{cand[6]} Years", f"{cand[4]} PLN"))


    # job_candidates = data.get_candidates()
    # for i in job_candidates:
    #     print(i)
    
    # # ── Populate rows in candidate table ────────────────────────────────────────────────────
    # for cand in job_candidates:
    #     create_hire_window.hire_selected()

def update_all_charts():
    update_candidates()
    # if staff_chart in active_charts:
    #     staff_chart.destroy()
    # if expenses_chart in active_charts:
    #     expenses_chart.destroy()
    # if money_chart in active_charts:
    #     money_chart.destroy()


# message box
def show_message():
    messagebox.showinfo("Informacja", "Twoja restauracja nadal istnieje. Dziwne.")

# overrite close button
def on_close():
    print("Zamykam restaurację...")  # Optional funeral message
    root.destroy()  # Closes the window
    root.quit()     # Stops the mainloop entirely


def test():
    print("TEST")

# ON READY: Everything below happens the moment program starts:

# table variables:


# Dummy candidate list (normally from SQL)
candidates_data = [
    {"name": "Jan Kowalski", "age": 28, "experience": "2 years"},
    {"name": "Anna Nowak", "age": 35, "experience": "5 years"},
    {"name": "Piotr Zieliński", "age": 22, "experience": "Intern"},
]

#create_main_window


# Create root window
root = tk.Tk()
root.title("MyBuisness By Maciej Wątor") 

# override the close button to kill the app
root.protocol("WM_DELETE_WINDOW", on_close)

# set the spawn location and size of the main window
root.geometry("320x600+10+10")  # 800x600 window, 200px from the left, 100px from the top

root.config(bg="#2d2d2d")  # Dark theme because we're edgy


# DISPLAY:

y_coord = 20

# Display the current money, that the user has at their disposal
today_label = tk.Label(root, text=f"Today: {data.today}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
today_label.place(x=20, y=y_coord) # controll the location
y_coord += 40

# Display the current money, that the user has at their disposal
money_label = tk.Label(root, text=f"Your Budget: {money}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
money_label.place(x=20, y=y_coord) # controll the location
y_coord += 40

# Display the expected change for the next month
expected_money_change_label = tk.Label(root, text=f"Estimated turnover: {expected_money_change}", font=("Helvetica", 16, "bold"), fg="red", bg="#2d2d2d")
expected_money_change_label.place(x=20, y=y_coord) # controll the location
y_coord += 40

staff_display = tk.Label(root, text=f"Your Current Staff: {currest_staff}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
staff_display.place(x=20, y=y_coord) # controll the location
y_coord += 40

staff_hire_display = tk.Label(root, text=f"{hiring_status}", font=("Helvetica", 16, "bold"), fg="green", bg="#2d2d2d")
staff_hire_display.place(x=20, y=y_coord) # controll the location
y_coord += 40


# BUTTONS:

# button to show the money chart
money_chart_btn = tk.Button(root, text="Show Money Chart!", command=show_money_chart, bg="#2500aa", fg="white")
money_chart_btn.place(x=10, y=y_coord) # controll the location of the button
y_coord += 40

# button to show the hiring window
hire_window_btn = tk.Button(root, text="Start Hiring", command=show_hire_window, bg="#0eaa00", fg="white")
hire_window_btn.place(x=10, y=y_coord) # controll the location of the button

# button to stop the hiring
stop_hire_window_btn = tk.Button(root, text="Stop Hiring", command=stop_hiring, bg="#aa0000", fg="white")
stop_hire_window_btn.place(x=10, y=y_coord) # controll the location of the button
stop_hire_window_btn.place_forget()

candidates_btn = tk.Button(root, text="See Candidates", command=show_candidates_window, bg="#8baa00", fg="white")
candidates_btn.place(x=100, y=y_coord) # controll the location of the button
y_coord += 40

# button to show the expenses chart
expenses_chart_btn = tk.Button(root, text="Show Expenses Chart!", command=show_expenses_chart, bg="#2500aa", fg="white")
expenses_chart_btn.place(x=10, y=y_coord) # controll the location of the button
y_coord += 40

# button to show the staff chart
staff_chart_btn = tk.Button(root, text="Show Staff Chart!", command=show_staff_chart, bg="#2500aa", fg="white")
staff_chart_btn.place(x=10, y=y_coord) # controll the location of the button
y_coord += 40

# button to progress to the next month
next_month_btn = tk.Button(root, text="Progress to next Month!", command=next_month, bg="#2500aa", fg="white")
next_month_btn.place(x=10, y=y_coord) # controll the location of the button
y_coord += 40


# create all sub-chart windows
create_expenses_chart()
create_money_chart()
create_staff_chart()
create_hire_window()
create_job_offer_window()

# then hide it
hide_all()

# Start the GUI loop
root.mainloop()