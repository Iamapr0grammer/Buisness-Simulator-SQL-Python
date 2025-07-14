from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import data, generator


## co dalej?
# Nadanie funkcjonalności grafowi wydatków, ten wykres kołowy, by przedstawiał faktycznie ilość wydatków.

# GLOBAL VARIABLES
money_chart   = None
money_canvas  = None
money_ax      = None
money_history = []      # ← keeps *all* months
POINT_PIXELS  = 120      # ≈ pixels per point on the x‑axis
MIN_POINTS    = 3
DPI = 100         # we created the figure with dpi=100


# job posting:
job_post_active = False
salary_offer = 0

# data:
currest_staff = 0 # the amount of staff currently working
hiring_status = "Not Hiring"
expected_money_change = data.next_month_change()
money = 1000000 # starting money

# === CHART FUNCTIONS ===


def create_money_chart():
    """Build the window & chart once; it auto‑resizes."""
    global money_chart, money_canvas, money_ax, fig

    money_chart = tk.Toplevel()
    money_chart.title("Money Chart")
    money_chart.geometry("500x400+350+50")
    money_chart.config(bg="#2d2d2d")
    money_chart.protocol("WM_DELETE_WINDOW", money_chart.withdraw)
    
    # I did not found any way to re-size it after the creation, so I will just...
    fig, money_ax = plt.subplots(figsize=(40, 20), dpi=100) # make the graphs so big, that the user will not see its ends
    fig.patch.set_facecolor("#2d2d2d")
    money_ax.set_facecolor("#2d2d2d")
    _style_money_ax()

    money_canvas = FigureCanvasTkAgg(fig, master=money_chart)
    money_canvas.draw()
    canvas_widget = money_canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True) 
    #canvas_widget.configure(background="#2d2d2d")

    # redraw every time user resizes the window
    canvas_widget.bind("<Configure>", _on_money_resize)


def update_money_chart():
    """Fetch fresh data and store in the history, then redraw."""
    global money_history

    rows = data.get_monthly_money_chart()         # list of (date, balance)
    money_history = rows                          # keep ALL months
    _redraw_visible_points()                      # draw slice fitting the width


# ──────────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────────

def _style_money_ax():
    """Common styling for the axis."""
    money_ax.set_title("Cash Over Time", color="white")
    money_ax.set_xlabel("Month",         color="white")
    money_ax.set_ylabel("PLN",           color="white")
    money_ax.tick_params(colors='white')


def _visible_count_for_width(width_px: int) -> int:
    """How many points can fit given window width (heuristic)."""
    return max(MIN_POINTS, width_px // POINT_PIXELS)


def _redraw_visible_points():
    """Slice history to what fits and refresh matplotlib canvas."""
    if not money_history:
        return
    
    # How wide is the canvas *right now*?
    width_px = money_canvas.get_tk_widget().winfo_width()
    n_points = _visible_count_for_width(width_px)

    # Slice last n_points
    slice_ = money_history[-n_points:]
    days   = [row[0] for row in slice_]
    money  = [row[1] for row in slice_]

    # draw
    money_ax.clear()
    money_ax.set_facecolor("#2d2d2d")
    _style_money_ax()
    money_ax.plot(days, money, color="lime", marker='o')
    money_canvas.draw()


def _on_money_resize(event):
    """Stretch the matplotlib figure to exactly fill the Tk canvas widget."""
    if event.width < 10 or event.height < 10:    # skip spurious tiny events
        return

    # inches = pixels / dpi
    new_w = event.width  / fig.dpi
    new_h = event.height / fig.dpi

    fig.set_size_inches(new_w, new_h, forward=True)   # forward=True ⇢ redraw
    fig.tight_layout()                                # use full area
    money_canvas.draw_idle()                          # cheaper than draw()

    _redraw_visible_points()




def create_expenses_chart():
    global expenses_chart
    print("create Expenses Chart")

    expenses_chart = tk.Toplevel()
    expenses_chart.title("Expenses Chart")
    expenses_chart.geometry("400x400+860+50")
    expenses_chart.config(bg="#2d2d2d")


    # Sample Data, just for creation, will be replaced instantly before the player has a chance to see it
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


def create_staff_window():
    global staff_window, staff_tree

    staff_window = tk.Toplevel()
    staff_window.title("Staff Controll Window")
    staff_window.geometry("600x400+350+510")
    staff_window.config(bg="#2d2d2d")

    # ── Treeview + scrollbar frame ───────────────────────────────────────
    frame = tk.Frame(staff_window, bg="#2d2d2d")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



    columns = ("name", "salary", "Vdays", "Jstart", "Reprimands")
    staff_tree = ttk.Treeview(
        frame, columns=columns, show="headings",
        yscrollcommand=scrollbar.set, selectmode="browse"
    )
    scrollbar.config(command=staff_tree.yview)

    # Headings
    staff_tree.heading("name",   text="Name")
    staff_tree.heading("salary", text="Salary")
    staff_tree.heading("Vdays", text="Vacation Days")
    staff_tree.heading("Jstart", text="Job Start")
    staff_tree.heading("Reprimands", text="Reprimands")

    # Column widths / alignment
    staff_tree.column("name",   width=50)
    staff_tree.column("salary",   width=50)
    staff_tree.column("Vdays",   width=50)
    staff_tree.column("Jstart",   width=50)
    staff_tree.column("Reprimands",   width=50)

    # tree.column("exp",   width=220)
    # tree.column("salary", width=120, anchor="center")

    staff_tree.pack(fill=tk.BOTH, expand=True)

    # ── Action buttons (Hire / Reject) ───────────────────────────────────
    btn_frame = tk.Frame(staff_window, bg="#2d2d2d")
    btn_frame.pack(pady=10)

    def hire_selected():
        selected = staff_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        hire_employee(cid)
        delete_candidate(cid)
        staff_tree.delete(cid)

    def reject_selected():
        selected = staff_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        staff_tree.delete(cid)
        delete_candidate(cid)

    hire_btn   = tk.Button(btn_frame, text="Hire",   width=12, bg="#008f39", fg="white",
                           command=hire_selected)
    reject_btn = tk.Button(btn_frame, text="Reject", width=12, bg="#cc0000", fg="white",
                           command=reject_selected)
    hire_btn.grid(row=0, column=0, padx=10)
    reject_btn.grid(row=0, column=1, padx=10)

    # overrite close button
    def staff_window_close():
        staff_window.withdraw()

    # override the close button to kill the app
    staff_window.protocol("WM_DELETE_WINDOW", staff_window_close)







# ── Window factory ────────────────────────────────────────────────────────
def create_hire_window():
    global hire_window, tree

    hire_window = tk.Toplevel()
    hire_window.title("Candidate List")
    hire_window.geometry("600x400+1040+510")
    hire_window.config(bg="#2d2d2d")

    # ── Treeview + scrollbar frame ───────────────────────────────────────
    frame = tk.Frame(hire_window, bg="#2d2d2d")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



    columns = ("name", "exp", "age", "salary")
    tree = ttk.Treeview(
        frame, columns=columns, show="headings",
        yscrollcommand=scrollbar.set, selectmode="browse"
    )
    scrollbar.config(command=tree.yview)

    # Headings
    tree.heading("name",   text="Name")
    tree.heading("exp",   text="Expirience")
    tree.heading("age",   text="Age")
    tree.heading("salary", text="Expected Salary")

    # Column widths / alignment
    tree.column("name",   width=180)
    tree.column("exp",   width=80)
    tree.column("age",   width=80)
    tree.column("salary", width=120, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)


    # ── Action buttons (Hire / Reject) ───────────────────────────────────
    btn_frame = tk.Frame(hire_window, bg="#2d2d2d")
    btn_frame.pack(pady=10)

    def hire_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        hire_employee(cid)
        delete_candidate(cid)
    
    def reject_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a candidate first.")
            return
        cid = int(selected[0])
        delete_candidate(cid)

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


def hire_employee(cid): # move the candidated from the candidates database to the staff database
    data.hire_employee(cid) # add the candidate to the staff database and delete the candidate form the candidate database
    update_all()

def delete_candidate(cid): # delete the candidate from the candidates database
    data.delete_candidate(cid)

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
        global job_post_active, salary_offer, root
        chosen = selected_salary.get()
        job_post_active = True
        stop_hire_window_btn.place(x=10, y=260)

        salary_offer = int(chosen)

        # update hiring status
        staff_hire_display.config(text="Hiring", fg="green")

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
    money_label.config(text=f"Your Budget: {money}")
    expected_money_change_label.config(text=f"Estimated turnover: {expected_money_change}")

    # change color based on espected change
    if expected_money_change < 0:
        expected_money_change_label.config(fg="red")
    else:
        expected_money_change_label.config(fg="green")
    
    # update the date
    today_label.config(text=f"Today: {data.today}")



def update_money(): # update the money that the player currently have
    global money
    expected_money_change = data.next_month_change()
    money = data.get_money()
    money += expected_money_change
    data.money_change(expected_money_change, "i have no idea why", data.today)
    




# show charts functions

def show_money_chart():
    money_chart.deiconify()
    

def show_expenses_chart():
    expenses_chart.deiconify()
    

def show_staff_chart():
    staff_window.deiconify()


# show window functions

def show_hire_window():
    job_offer.deiconify()

def show_candidates_window():
    staff_window.deiconify()

def show_candidates_button():
    pass

def hide_candidates_button():
    pass

# a button to hide/reveal all windows with just one click
def hide_all():
    pass

# === MAIN WINDOW ===

def next_month():
    data.next_month()

    # generate all events, before UI is updated
    if job_post_active:
        candidates = generator.chance_for_new_candidate(salary_offer) # generates new candidates and places them inside the database
        data.add_candidates(candidates)
    
    update_money()
    update_all()



def stop_hiring():
    global job_post_active, root
    #candidates_btn.place(x=100, y=260)
    stop_hire_window_btn.place_forget()

    # job posting:
    job_post_active = False

    # update hiring status
    staff_hire_display.config(text="Not Hiring", fg="red")

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

        full_name = str(cand[1] + " " + cand[2])
        id = cand[0]

        tree.insert("", tk.END, iid=id,
                    values=(full_name, f"{cand[6]} Years", cand[5] ,f"{cand[4]} PLN"))


def update_all():

    generator.generate_random_expanses(data.today) # temporary for testing, delete later if necessary

    update_candidates() # add candidates from the database
    update_staff() # update the small window with the staff
    update_display() # the main root chart
    
    update_money_chart() # update the chart with money over time


def update_staff():
    # 1) fetch all staff ------------------------------------------------
    staff = data.get_staff()   # expects list of tuples / dicts

    # 2) clear current table -------------------------------------------
    staff_tree.delete(*staff_tree.get_children())

    # 3) insert rows ----------------------------------------------------
    for employee in staff:
        # adapt to your real tuple / dict shape:

        employee_id = employee[0]
        employee_full_name = str(employee[1] + " " + employee[2])
        employee_salary = employee[3]
        employee_vacation_days = employee[4]
        employee_job_start = employee[6]
        employee_reprimands = employee[10]

        staff_tree.insert("", tk.END, iid=employee_id,
                    values=(employee_full_name, f"{employee_salary} PLN", employee_vacation_days, employee_job_start, employee_reprimands))


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

staff_hire_display = tk.Label(root, text=f"{hiring_status}", font=("Helvetica", 16, "bold"), fg="red", bg="#2d2d2d")
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
create_staff_window()
create_hire_window()
create_job_offer_window()

# then hide it
hide_all()

# Start the GUI loop
root.mainloop()