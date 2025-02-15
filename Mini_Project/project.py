import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"


class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts)

    def save_data(self, filename):
        try:
            with open(filename, 'w') as file:
                for workout in self.workouts:
                    file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(',')
                    workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                    self.workouts.append(workout)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False


class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Fitness Tracker")
        
        self.user = None
        
        # Set a background color
        self.root.config(bg="#F0F8FF")  # Light blue background
        
        self.create_widgets()

    def create_widgets(self):
        # Create labels and entries with colors
        self.name_label = tk.Label(self.root, text="Name:", bg="#F0F8FF", fg="#4B0082", font=("Arial", 12, "bold"))
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="#E6E6FA", fg="#4B0082")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.age_label = tk.Label(self.root, text="Age:", bg="#F0F8FF", fg="#4B0082", font=("Arial", 12, "bold"))
        self.age_label.grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="#E6E6FA", fg="#4B0082")
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(self.root, text="Weight:", bg="#F0F8FF", fg="#4B0082", font=("Arial", 12, "bold"))
        self.weight_label.grid(row=2, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="#E6E6FA", fg="#4B0082")
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons with background colors
        self.create_user_button = tk.Button(self.root, text="Create User", command=self.create_user, bg="#8A2BE2", fg="white", font=("Arial", 12, "bold"))
        self.create_user_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_workout_button = tk.Button(self.root, text="Add Workout", command=self.add_workout, bg="#32CD32", fg="white", font=("Arial", 12, "bold"))
        self.add_workout_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.view_workouts_button = tk.Button(self.root, text="View Workouts", command=self.view_workouts, bg="#FF6347", fg="white", font=("Arial", 12, "bold"))
        self.view_workouts_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.save_data_button = tk.Button(self.root, text="Save Data", command=self.save_data, bg="#FFD700", fg="black", font=("Arial", 12, "bold"))
        self.save_data_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.load_data_button = tk.Button(self.root, text="Load Data", command=self.load_data, bg="#20B2AA", fg="white", font=("Arial", 12, "bold"))
        self.load_data_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Listbox to display workouts
        self.workout_listbox = tk.Listbox(self.root, width=50, height=10, bg="#E6E6FA", fg="#4B0082", font=("Arial", 10), selectbackground="#ADD8E6")
        self.workout_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    def create_user(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        weight = float(self.weight_entry.get())
        self.user = User(name, age, weight)
        messagebox.showinfo("Success", "User created successfully!")

    def add_workout(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
        exercise_type = simpledialog.askstring("Input", "Enter the exercise type:")
        duration = int(simpledialog.askstring("Input", "Enter the duration (minutes):"))
        calories_burned = int(simpledialog.askstring("Input", "Enter the calories burned:"))

        workout = Workout(date, exercise_type, duration, calories_burned)
        self.user.add_workout(workout)
        self.update_workout_list()
        messagebox.showinfo("Success", "Workout added successfully!")

    def view_workouts(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        workouts = self.user.view_workouts()
        self.workout_listbox.delete(0, tk.END)
        if workouts:
            for workout in workouts.split("\n"):
                self.workout_listbox.insert(tk.END, workout)
        else:
            self.workout_listbox.insert(tk.END, "No workouts available.")

    def save_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            if self.user.save_data(filename):
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save data.")

    def load_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            if self.user.load_data(filename):
                messagebox.showinfo("Success", "Data loaded successfully!")
                self.update_workout_list()
            else:
                messagebox.showerror("Error", "Failed to load data or file not found.")

    def update_workout_list(self):
        self.workout_listbox.delete(0, tk.END)
        if self.user.workouts:
            for workout in self.user.workouts:
                self.workout_listbox.insert(tk.END, str(workout))
        else:
            self.workout_listbox.insert(tk.END, "No workouts available.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
