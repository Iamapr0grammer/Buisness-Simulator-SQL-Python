import tkinter as tk
from tkinter import ttk, messagebox

# ── Dummy data ────────────────────────────────────────────────────────────
candidates = [
    {"id": 1, "name": "Jan Kowalski",   "qual": "Chef, 3 yrs", "salary": 3500},
    {"id": 2, "name": "Anna Nowak",     "qual": "Waitress, 2 yrs", "salary": 2900},
    {"id": 3, "name": "Piotr Zieliński","qual": "Bartender, 4 yrs", "salary": 3200},
    {"id": 4, "name": "Olga Wiśniewska","qual": "Sous‑Chef, 6 yrs","salary": 4200},
    {"id": 5, "name": "Krzysztof Żuk",  "qual": "Cleaner, 1 yr",   "salary": 2400},
    # …add as many as you like
]
hired_ids = set()   # store hired candidate IDs


# ── Window factory ────────────────────────────────────────────────────────
def show_candidates_window():

    win = tk.Toplevel()
    win.title("Candidate List")
    win.geometry("600x400+500+200")
    win.config(bg="#2d2d2d")

    # ── Treeview + scrollbar frame ───────────────────────────────────────
    frame = tk.Frame(win, bg="#2d2d2d")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ("name", "qual", "salary")
    tree = ttk.Treeview(
        frame, columns=columns, show="headings",
        yscrollcommand=scrollbar.set, selectmode="browse"
    )
    scrollbar.config(command=tree.yview)

    # Headings
    tree.heading("name",   text="Name")
    tree.heading("qual",   text="Qualification")
    tree.heading("salary", text="Expected Salary")

    # Column widths / alignment
    tree.column("name",   width=180)
    tree.column("qual",   width=220)
    tree.column("salary", width=120, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    # ── Populate rows ────────────────────────────────────────────────────
    for cand in candidates:
        text_salary = f"{cand['salary']} PLN"
        tree.insert("", tk.END, iid=cand["id"],
                    values=(cand["name"], cand["qual"], text_salary))

    # ── Action buttons (Hire / Reject) ───────────────────────────────────
    btn_frame = tk.Frame(win, bg="#2d2d2d")
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


# ── Demo root ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150+100+100")
    root.title("Evil HR Console")

    open_btn = tk.Button(root, text="View Candidates",
                         command=show_candidates_window,
                         bg="#8baa00", fg="white")
    open_btn.pack(expand=True)

    root.mainloop()
