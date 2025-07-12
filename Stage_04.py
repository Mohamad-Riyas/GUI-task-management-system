# Author : Riyas
# Date : 18th APR 2025

# Stage 04 : Tkinter GUI for Viewing, Searching, and Sorting Tasks

import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -------------------- Task Class --------------------

# Represents a single task with name, description, priority, and due date
class Task:
    def __init__(self, name, description, priority, due_date,):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        
    # Convert Task object to dictionary for saving in JSON
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }

    # Create a Task object from dictionary 
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            task_dict["name"],
            task_dict["description"],
            task_dict["priority"],
            task_dict["due_date"],
        )

# -------------------- Task Manager Class --------------------

# Handles task list management including file operations, filtering, and sorting
class TaskManager:
    def __init__(self, json_file='tasks.json'):
        self.tasks = []
        self.json_file = json_file
        self.load_tasks_from_json()

    # Load tasks from the JSON file
    def load_tasks_from_json(self):
        try:
            with open(self.json_file, "r") as file:
                task_dicts = json.load(file)
                self.tasks = [Task.from_dict(task_dict) for task_dict in task_dicts]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")

    # Save current tasks to the JSON file
    def save_tasks_to_json(self):
        try:
            with open(self.json_file, "w") as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    # Add a new task
    def add_task(self, task_data):
        task = Task(**task_data)
        self.tasks.append(task)
        self.save_tasks_to_json()
        return task

    # Update an existing task by index
    def update_task(self, index, task_data):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            for key, value in task_data.items():
                setattr(task, key, value)
            self.save_tasks_to_json()
            return True
        return False

    # Delete a task by index
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks_to_json()
            return True
        return False

    # Filter tasks by name, priority, and due date
    def filter_tasks(self, name="", priority="All", date=""):
        tasks = self.tasks
        if name:
            tasks = [t for t in tasks if name.lower() in t.name.lower()]
        if priority != "All":
            tasks = [t for t in tasks if t.priority == priority]
        if date:
            tasks = [t for t in tasks if t.due_date == date]
        return tasks

    # Sort tasks by name, due_date, or priority
    def sort_tasks(self, key, reverse=False):
        if key == "priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            self.tasks.sort(key=lambda t: priority_order.get(t.priority, 3), reverse=reverse)
        elif key == "due_date":
            self.tasks.sort(key=lambda t: datetime.strptime(t.due_date, "%Y-%m-%d"), reverse=reverse)
        else:
            self.tasks.sort(key=lambda t: getattr(t, key).lower(), reverse=reverse)
        return self.tasks

# -------------------- Task Manager GUI Class --------------------

# Builds the main application GUI using Tkinter
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.root.geometry("1024x768")
        self.root.configure(bg='#f0f0f0')

        self.manager = TaskManager() # Task manager instance
        self.current_sort = {"key": "name", "reverse": False}  # Default sort state

        self.setup_ui()  # Setup GUI components
        self.refresh_tasks()  # Load and show tasks

    # Setup all the UI widgets and layout
    def setup_ui(self):
        
        style = ttk.Style()
        style.configure('TFrame', background='#4a90d9')
        style.configure('TLabel', background='#e1e1e1')
        style.configure('TButton', background='#4a90d9')
        style.configure('TLabelframe', background='#252526')
        style.configure('TLabelframe.Label', background='#f0f0f0')
        
        
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, 
                               text="Personal Task Manager", 
                               font=('Helvetica', 20, 'bold italic underline'),
                               background='#5cb85c')
        title_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Filter Section
        filter_frame = ttk.LabelFrame(main_frame, text="Filters", padding=10)
        filter_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)

        # Filter inputs
        ttk.Label(filter_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_filter = ttk.Entry(filter_frame)
        self.name_filter.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Priority:").grid(row=0, column=2, padx=5)
        self.priority_filter = ttk.Combobox(filter_frame, values=["All", "High", "Medium", "Low"])
        self.priority_filter.current(0)
        self.priority_filter.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5)
        self.date_filter = ttk.Entry(filter_frame)
        self.date_filter.grid(row=0, column=5, padx=5)

        ttk.Button(filter_frame, text="Apply", command=self.apply_filters).grid(row=0, column=6, padx=5)
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).grid(row=0, column=7, padx=5)

        # Task List (Treeview)
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")
        style.map('Treeview', background=[('selected', '#4a90d9')])
        style.configure('TCombobox', fieldbackground='white', background='white')
        style.configure('TCombobox', arrowcolor='black')
        style.configure('TEntry', fieldbackground='white')

        self.tree = ttk.Treeview(tree_frame, columns=("name", "description", "priority", "due_date"),
                                show="headings", selectmode="browse")

        # Treeview column headings with sorting on click
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title(),
                            command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=120 if col != "description" else 250)

        # Scrollbar for task list
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(btn_frame, text="Add Task", command=self.show_add_dialog).pack(side="top", padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=self.show_edit_dialog).pack(side="top", padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side="top", padx=5)

        # Allow task list to expand with the window
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    # Refresh task list in Treeview
    def refresh_tasks(self, tasks=None):
        self.tree.delete(*self.tree.get_children())
        tasks = tasks if tasks is not None else self.manager.tasks
        for task in tasks:
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date))

    # Apply filters and show filtered tasks
    def apply_filters(self):
        tasks = self.manager.filter_tasks(
            name=self.name_filter.get(),
            priority=self.priority_filter.get(),
            date=self.date_filter.get()
        )
        self.refresh_tasks(tasks)

    # Clear all filters and show all tasks
    def clear_filters(self):
        self.name_filter.delete(0, tk.END)
        self.priority_filter.current(0)
        self.date_filter.delete(0, tk.END)
        self.refresh_tasks()

    # Sort tasks by selected column
    def sort_by_column(self, column):
        if self.current_sort["key"] == column:
            self.current_sort["reverse"] = not self.current_sort["reverse"]
        else:
            self.current_sort = {"key": column, "reverse": False}
        self.manager.sort_tasks(column, self.current_sort["reverse"])
        self.refresh_tasks()

    # Show dialog to add a new task
    def show_add_dialog(self):
        self.task_dialog("Add Task", self.add_task)

    # Show dialog to edit selected task
    def show_edit_dialog(self):
        if not self.tree.selection():
            messagebox.showinfo("Info", "Please select a task to edit")
            return
        index = self.tree.index(self.tree.selection()[0])
        task = self.manager.tasks[index]
        self.task_dialog("Edit Task", self.update_task, index, task)

    # Common dialog window for both add/edit task
    def task_dialog(self, title, callback, index=None, task=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#f0f0f0')

        fields = {}
        labels = ["Name", "Description", "Priority", "Due Date (YYYY-MM-DD):"]
        keys = ["name", "description", "priority", "due_date"]

        for i, (label, key) in enumerate(zip(labels, keys)):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            if key == "priority":
                fields[key] = ttk.Combobox(dialog, values=["High", "Medium", "Low"])
                fields[key].current(1)
            elif key == "description":
                fields[key] = tk.Text(dialog, height=5, width=30, bg='white')
            else:
                fields[key] = ttk.Entry(dialog)

            fields[key].grid(row=i, column=1, padx=5, pady=5, sticky="we")
            if task:
                if key == "description":
                    fields[key].insert("1.0", getattr(task, key))
                else:
                    fields[key].insert(0, getattr(task, key))

        # Save and Cancel buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Save", style='TButton', command=lambda: self.save_task(
            dialog, fields, callback, index)).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", style='TButton', command=dialog.destroy).pack(side="left", padx=5)

    # Save task from dialog input
    def save_task(self, dialog, fields, callback, index=None):
        data = {
            "name": fields["name"].get().strip(),
            "description": fields["description"].get("1.0", tk.END).strip(),
            "priority": fields["priority"].get(),
            "due_date": fields["due_date"].get().strip(),
        }

        if not data["name"]:
            messagebox.showerror("Error", "Task name is required")
            return

        try:
            datetime.strptime(data["due_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format (use YYYY-MM-DD)")
            return

        # Call add or update based on the context
        if index is None:
            callback(data)
        else:
            callback(index, data)

        dialog.destroy()
        self.refresh_tasks()

    # Add task wrapper
    def add_task(self, task_data):
        self.manager.add_task(task_data)

    # Update task wrapper
    def update_task(self, index, task_data):
        self.manager.update_task(index, task_data)

    # Delete selected task
    def delete_task(self):
        if not self.tree.selection():
            messagebox.showinfo("Info", "Please select a task to delete")
            return

        index = self.tree.index(self.tree.selection()[0])
        task = self.manager.tasks[index]

        if messagebox.askyesno("Confirm", f"Delete task '{task.name}'?"):
            if self.manager.delete_task(index):
                self.refresh_tasks()
            else:
                messagebox.showerror("Error", "Failed to delete task")
        
# -------------------- Run the Application --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()