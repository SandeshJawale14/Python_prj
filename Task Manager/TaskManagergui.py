import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"


# Load tasks from a JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Handle case where file is empty or corrupted
            print(
                "Warning: tasks.json is empty or corrupted. Starting with an empty task list."
            )
            return []
    return []


# Save tasks to a JSON file
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)


# Global list to store tasks
tasks = load_tasks()


# Add a task
def add_task():
    task = task_entry.get()
    if task:
        tasks.append({"task": task, "completed": False})
        task_entry.delete(0, tk.END)
        update_tasks()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")


# Delete a task
def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = tasks.pop(selected_task_index[0])
        update_tasks()
        save_tasks()
        messagebox.showinfo("Task Deleted", f'Task "{task["task"]}" has been deleted.')
    else:
        messagebox.showwarning("Warning", "No task selected!")


# Mark a task as completed
def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = tasks[selected_task_index[0]]
        task["completed"] = True
        update_tasks()
        save_tasks()
        messagebox.showinfo(
            "Task Completed", f'Task "{task["task"]}" has been marked as completed.'
        )
    else:
        messagebox.showwarning("Warning", "No task selected!")


# Update the task list in the Listbox
def update_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        task_listbox.insert(tk.END, f'{task["task"]} [{status}]')


# Clear all tasks
def clear_all_tasks():
    if messagebox.askyesno(
        "Clear All Tasks", "Are you sure you want to clear all tasks?"
    ):
        tasks.clear()
        update_tasks()
        save_tasks()


# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x400")

# Title Label
title_label = tk.Label(root, text="Task Manager", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Task Entry and Button
task_label = tk.Label(root, text="Enter a task:")
task_label.pack(pady=5)

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

# Task Listbox and Buttons
task_listbox = tk.Listbox(root, width=40, height=10, selectmode=tk.SINGLE)
task_listbox.pack(pady=5)

complete_button = tk.Button(root, text="Complete Task", command=complete_task)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All Tasks", command=clear_all_tasks)
clear_button.pack(pady=5)

# Update task list on start
update_tasks()

# Start the main loop
root.mainloop()
