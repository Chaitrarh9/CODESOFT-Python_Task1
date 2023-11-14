import sqlite3
import tkinter.messagebox
from tkinter import *

# Create or connect to a database
conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS tasks 
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
           task TEXT)
          ''')
conn.commit()


def save_task_to_db(task):
    c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()


def load_tasks_from_db():
    c.execute('SELECT task FROM tasks')
    return c.fetchall()


def update_database():
    # Delete all rows in the current table
    c.execute('DELETE FROM tasks')
    conn.commit()

    # Insert all tasks from the listbox into the database
    for task in listbox_task.get(0, END):
        save_task_to_db(task[2:])

    tkinter.messagebox.showinfo("Success", "Database updated successfully.")


def on_closing():
    confirmation = tkinter.messagebox.askyesno("Confirmation",
                                               "Are you sure you want to exit? Changes will be lost if not updated.")
    if confirmation:
        window.destroy()


def entertask():
    def add():
        input_text = entry_task.get(1.0, "end-1c")
        if input_text.strip():  # Check if the input is not empty or just whitespace
            tasks = input_text.split("\n")
            for task in tasks:
                if task.strip():  # Check if the task is not just whitespace
                    save_task_to_db(task)
            update_task_bullet_points()
            root1.destroy()

    root1 = Tk()
    root1.title("Add task")
    root1.geometry("600x400")
    root1.configure(bg="#2c3e50")

    entry_task = Text(root1, width=60, height=8, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
    entry_task.pack(pady=20)

    button_temp = Button(root1, text="Add task", command=add, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    button_temp.pack(pady=10)

    root1.mainloop()


def deletetask():
    selected = listbox_task.curselection()
    if not selected:
        tkinter.messagebox.showinfo("Information", "Please select a task to delete.")
        return

    confirmation = tkinter.messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected task?")
    if confirmation:
        listbox_task.delete(selected)


def markcompleted():
    marked = listbox_task.curselection()
    if not marked:
        tkinter.messagebox.showinfo("Information", "Please select a task to mark as completed.")
        return

    temp = marked[0]
    temp_marked = listbox_task.get(temp)
    if "✔" not in temp_marked:
        temp_marked = temp_marked + " ✔"
        listbox_task.delete(temp)
        listbox_task.insert(temp, temp_marked)
    else:
        tkinter.messagebox.showinfo("Information", "Task is already marked as completed.")


def update_task_bullet_points():
    listbox_task.delete(0, END)
    for task in load_tasks_from_db():
        listbox_task.insert(END, f"• {task[0]}")


window = Tk()
window.title("To-Do List Application")
window.geometry("800x600")
window.configure(bg="#2c3e50")

frame_task = Frame(window, bg="#34495e", bd=5, relief=GROOVE)
frame_task.pack(pady=20)

listbox_task = Listbox(frame_task, bg="#ecf0f1", fg="#2c3e50", height=15, width=60, font=("Arial", 14),
                       selectbackground="#3498db", selectforeground="white", bd=0, activestyle="none")

# Adding vertical scrollbar inside the listbox with a different color
scrollbar_vertical_listbox = Scrollbar(frame_task, orient=VERTICAL, bd=0, troughcolor="#3498db",
                                       activebackground="#3498db")
scrollbar_vertical_listbox.pack(side=RIGHT, fill=Y)

listbox_task.config(yscrollcommand=scrollbar_vertical_listbox.set)

scrollbar_vertical_listbox.config(command=listbox_task.yview)

listbox_task.pack(side=LEFT, pady=10)

entry_button = Button(window, text="Add task", width=20, command=entertask, bg="#2ecc71", fg="white",
                      font=("Helvetica", 16, "bold"))
entry_button.pack(pady=10)

delete_button = Button(window, text="Delete selected task", width=20, command=deletetask, bg="#e74c3c", fg="white",
                       font=("Helvetica", 16, "bold"))
delete_button.pack(pady=10)

mark_button = Button(window, text="Mark as completed", width=20, command=markcompleted, bg="#f39c12", fg="white",
                     font=("Helvetica", 16, "bold"))
mark_button.pack(pady=10)

update_button = Button(window, text="Update", width=20, command=update_database, bg="#3498db", fg="white",
                       font=("Helvetica", 16, "bold"))
update_button.pack(pady=10)

# Load tasks from the database on startup
update_task_bullet_points()

# Bind the on_closing function to the window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
