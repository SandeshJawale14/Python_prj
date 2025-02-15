import sys
import json
import os
from datetime import datetime

tasks = []


# Load tasks from a file
def load_tasks():
    try:
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                global tasks
                tasks = json.load(file)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Error: Corrupted tasks file. Creating a new one.")
        tasks.clear()


# Save tasks to a file
def save_tasks():
    try:
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError:
        print("Error: Could not save tasks. Please check file permissions.")


# Add a new task
def add_task(task, due_date=None, priority=None, category=None):
    task_details = {
        "task": task,
        "completed": False,
        "due_date": due_date,
        "priority": priority,
        "category": category,
    }
    tasks.append(task_details)
    print(f"Added task: {task}")


# Delete a task by its index
def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        print(f'Deleted task: {removed_task["task"]}')
    except IndexError:
        print("Invalid task number. Please check the task list.")


# View all tasks with formatting
def view_tasks():
    if not tasks:
        print("No tasks available")
    else:
        for i, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            # Add colors to output for better UX
            status_color = "\033[32m" if task["completed"] else "\033[31m"
            print(
                f'{i + 1}. {task["task"]} [{status_color}{status}\033[0m] - Due: {due_date} - Priority: {priority} - Category: {category}'
            )


# Mark a task as completed
def mark_task_completed(task_index):
    try:
        tasks[task_index]["completed"] = True
        print(f'Marked task as completed: {tasks[task_index]["task"]}')
    except IndexError:
        print("Invalid task number")


# Mark a task as incomplete
def mark_task_incomplete(task_index):
    try:
        tasks[task_index]["completed"] = False
        print(f'Marked task as incomplete: {tasks[task_index]["task"]}')
    except IndexError:
        print("Invalid task number")


# Search tasks by keyword
def search_tasks(keyword):
    results = [task for task in tasks if keyword.lower() in task["task"].lower()]
    if not results:
        print("No matching tasks found")
    else:
        for i, task in enumerate(results):
            status = "Completed" if task["completed"] else "Pending"
            due_date = task["due_date"] if task["due_date"] else "No due date"
            priority = task["priority"] if task["priority"] else "No priority"
            category = task["category"] if task["category"] else "No category"
            status_color = "\033[32m" if task["completed"] else "\033[31m"
            print(
                f'{i + 1}. {task["task"]} [{status_color}{status}\033[0m] - Due: {due_date} - Priority: {priority} - Category: {category}'
            )


# Edit a task by its index
def edit_task(task_index):
    try:
        task = tasks[task_index]
        print(f"Editing task: {task['task']}")
        task["task"] = (
            input(f"New task description (current: {task['task']}): ").strip()
            or task["task"]
        )
        task["due_date"] = input(
            f"New due date (current: {task.get('due_date', 'No due date')}): "
        ).strip() or task.get("due_date")
        task["priority"] = input(
            f"New priority (current: {task.get('priority', 'No priority')}): "
        ).strip() or task.get("priority")
        task["category"] = input(
            f"New category (current: {task.get('category', 'No category')}): "
        ).strip() or task.get("category")
        print(f"Task updated: {task}")
    except IndexError:
        print("Invalid task number")


# Validate date format (YYYY-MM-DD)
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Show help instructions
def show_help():
    print(
        """
    Available commands:
    - add <task> <due_date (YYYY-MM-DD)> <priority> <category>: Add a new task with optional due date, priority, and category
    - delete <task_number>: Delete a task by its number
    - view: View all tasks
    - complete <task_number>: Mark a task as completed
    - incomplete <task_number>: Mark a task as incomplete
    - search <keyword>: Search for tasks by keyword
    - edit <task_number>: Edit an existing task
    - help: Show this help message
    - exit: Exit the application
    """
    )


# Main function to handle input and commands
def main():
    print("Task Manager Application")
    load_tasks()
    show_help()

    while True:
        command = input("Enter command: ").strip().split()

        if not command:
            continue

        if command[0] == "add":
            task = " ".join(command[1:])
            due_date = input(
                "Enter due date (YYYY-MM-DD) or press enter to skip: "
            ).strip()
            if due_date and not is_valid_date(due_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            priority = input(
                "Enter priority (High/Medium/Low) or press enter to skip: "
            ).strip()
            category = input("Enter category or press enter to skip: ").strip()
            add_task(
                task,
                due_date if due_date else None,
                priority if priority else None,
                category if category else None,
            )

        elif command[0] == "delete":
            if len(command) > 1 and command[1].isdigit():
                delete_task(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "view":
            view_tasks()

        elif command[0] == "complete":
            if len(command) > 1 and command[1].isdigit():
                mark_task_completed(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "incomplete":
            if len(command) > 1 and command[1].isdigit():
                mark_task_incomplete(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "search":
            if len(command) > 1:
                search_tasks(" ".join(command[1:]))
            else:
                print("Invalid command")

        elif command[0] == "edit":
            if len(command) > 1 and command[1].isdigit():
                edit_task(int(command[1]) - 1)
            else:
                print("Invalid command")

        elif command[0] == "help":
            show_help()

        elif command[0] == "exit":
            save_tasks()
            print("Exiting the application. Goodbye!")
            sys.exit()

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
