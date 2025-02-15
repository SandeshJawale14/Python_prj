import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from datetime import datetime

tasks = []


# Add Task
def add_task():
    task = task_entry.get()
    if task:
        due_date = askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:")
        priority = askstring(
            "Priority", "Enter priority (High/Medium/Low) or leave blank:"
        )
        category = askstring("Category", "Enter category or leave blank:")

        # Input validation for due date (check if it's in valid date format)
        if due_date and not is_valid_date(due_date):
            messagebox.showerror(
                "Invalid Date", "Please enter the due date in the format YYYY-MM-DD."
            )
            return

        task_details = {
            "task": task,
            "completed": False,
            "due_date": due_date if due_date else "No due date",
            "priority": priority if priority else "No priority",
            "category": category if category else "No category",
        }
        tasks.append(task_details)
        update_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")


# Check if the date is in the correct format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Delete Task
def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")


# Toggle task completion status (mark as completed or incomplete)
def toggle_task_completion():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = tasks[selected_task_index[0]]
        task["completed"] = not task["completed"]
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")


# Search tasks by keyword
def search_tasks():
    keyword = search_entry.get()
    if keyword:
        search_results = [
            task for task in tasks if keyword.lower() in task["task"].lower()
        ]
        task_listbox.delete(0, tk.END)
        for task in search_results:
            status = "Completed" if task["completed"] else "Pending"
            task_listbox.insert(
                tk.END,
                f'{task["task"]} [{status}] - Due: {task["due_date"]} - Priority: {task["priority"]} - Category: {task["category"]}',
            )
    else:
        messagebox.showwarning("Warning", "Search keyword cannot be empty!")


# Update Task List
def update_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        color = get_task_color(task)
        task_listbox.insert(
            tk.END,
            f'{task["task"]} [{status}] - Due: {task["due_date"]} - Priority: {task["priority"]} - Category: {task["category"]}',
        )
        task_listbox.itemconfig(tk.END, {"bg": color})


# Get color based on task priority and completion status
def get_task_color(task):
    if task["completed"]:
        return "lightgreen"
    elif task["priority"] == "High":
        return "lightcoral"
    elif task["priority"] == "Medium":
        return "lightyellow"
    return "white"


# Clear All Tasks
def clear_all_tasks():
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
        tasks.clear()
        update_tasks()


# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x500")  # Set the window size

# Create a stylish frame
frame = ttk.Frame(root, padding="10")
frame.pack(fill="both", expand=True)

# Create and place the widgets
task_label = ttk.Label(frame, text="Enter a task:")
task_label.grid(row=0, column=0, padx=5, pady=5)

task_entry = ttk.Entry(frame, width=50)
task_entry.grid(row=0, column=1, padx=5, pady=5)

add_button = ttk.Button(frame, text="Add Task", command=add_task)
add_button.grid(row=1, column=0, columnspan=2, pady=5)

delete_button = ttk.Button(frame, text="Delete Task", command=delete_task)
delete_button.grid(row=2, column=0, columnspan=2, pady=5)

complete_button = ttk.Button(
    frame, text="Toggle Completion", command=toggle_task_completion
)
complete_button.grid(row=3, column=0, columnspan=2, pady=5)

search_label = ttk.Label(frame, text="Search tasks:")
search_label.grid(row=4, column=0, padx=5, pady=5)

search_entry = ttk.Entry(frame, width=50)
search_entry.grid(row=4, column=1, padx=5, pady=5)

search_button = ttk.Button(frame, text="Search", command=search_tasks)
search_button.grid(row=5, column=0, columnspan=2, pady=5)

clear_button = ttk.Button(frame, text="Clear All Tasks", command=clear_all_tasks)
clear_button.grid(row=6, column=0, columnspan=2, pady=5)

task_listbox = tk.Listbox(
    frame, width=70, height=15, selectmode=tk.SINGLE, activestyle="none"
)
task_listbox.grid(row=7, column=0, columnspan=2, pady=10)

# Add some padding to the UI for cleaner spacing
for widget in frame.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# Start the main loop
root.mainloop()
