
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk



## co dalej?
# zrób, by okienka się pojawiały, gdy kilkniesz przycisk, i znikały po kliknięciu X. Ale, dodaj to tak, by przycisk następnego dnia, kasował wszystkie okienka,
# i jeśli jakieś było otwarte, to otwierał je na nowo. Potrzebuje tego, by resetować tabelki przy każdym nowym dniu. Później dodam, by otwierały się w tym samym
# miejscu, w jakim były zamknięte!




# === CHART FUNCTIONS ===

def show_money_chart():
    global active_charts
    print("Show Money Chart")

    # Create subwindow
    money_chart = tk.Toplevel()
    money_chart.title("Money Chart")
    money_chart.geometry("400x400+350+50")
    money_chart.config(bg="#2d2d2d")

    # add it to the list of active charts
    active_charts.append(money_chart)

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





def show_expenses_chart():
    global active_charts
    print("Show Expenses Chart")

    expenses_chart = tk.Toplevel()
    expenses_chart.title("Expenses Chart")
    expenses_chart.geometry("400x400+450+100")
    expenses_chart.config(bg="#2d2d2d")

    # add it to the list of active charts
    active_charts.append(expenses_chart)

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




def show_staff_chart():
    global active_charts
    print("Show Staff Chart")

    staff_chart = tk.Toplevel()
    staff_chart.title("Staff Chart")
    staff_chart.geometry("400x400+550+150")
    staff_chart.config(bg="#2d2d2d")

    # add it to the list of active charts
    active_charts.append(staff_chart)

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




# === MAIN WINDOW ===

def next_day():
    update_all_charts()
    


def update_all_charts():
    pass
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


# Create root window
root = tk.Tk()
root.title("MyBuisness By Maciej Wątor") 

# override the close button to kill the app
root.protocol("WM_DELETE_WINDOW", on_close)

# set the spawn location and size of the main window
root.geometry("300x600+10+10")  # 800x600 window, 200px from the left, 100px from the top

root.config(bg="#2d2d2d")  # Dark theme because we're edgy


# button to show the money chart
money_chart_btn = tk.Button(root, text="Show Money Chart!", command=show_money_chart, bg="#aa0000", fg="white")
money_chart_btn.pack(pady=10)
money_chart_btn.place(x=10, y=10) # controll the location of the button

# button to show the expenses chart
money_chart_btn = tk.Button(root, text="Show Expenses Chart!", command=show_expenses_chart, bg="#aa0000", fg="white")
money_chart_btn.pack(pady=10)
money_chart_btn.place(x=10, y=60) # controll the location of the button

# button to show the staff chart
money_chart_btn = tk.Button(root, text="Show Staff Chart!", command=show_staff_chart, bg="#aa0000", fg="white")
money_chart_btn.pack(pady=10)
money_chart_btn.place(x=10, y=110) # controll the location of the button

# button to progress to the next day
money_chart_btn = tk.Button(root, text="Next Day!", command=next_day, bg="#aa0000", fg="white")
money_chart_btn.pack(pady=10)
money_chart_btn.place(x=10, y=200) # controll the location of the button



# Start the GUI loop
root.mainloop()



