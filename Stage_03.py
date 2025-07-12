# Author: Riyas
# Date: 12th APR 2025

# Stage 3 : Using Dictionaries and JSON File Handling

import json

# list to store tasks

tasks = []

# Functions for CRUD operations


def add_task():
    """Add a new task to the list."""
    print("\n==== Add a New Task ====")

    # Get task details from user 
    task_name = input("Enter task name : ")
    task_description = input("Enter task description : ")

    # Validate priority input
    while True:
        priority = input("Enter task priority (High/Medium/Low): ").capitalize()
        if priority == "High" or priority == "Medium" or priority == "Low" :
            break
        print("Invalid Priority! Enter High , Medium or Low. ")
    
    # Validate due date input
    while True:
        due_date = input("Enter task due date (YYYY-MM-DD): ")
        if len(due_date)==10 and due_date[4]== "-" and due_date[-3] == "-":
            try:
                year = int(due_date[0:4])
                month = int(due_date[5:7])
                day = int(due_date[8:10])
                if 1 <= month <= 12 and 1 <= day <= 31:
                    break
            except ValueError:
                pass
        print("Invalid Due Date! Enter valid due date in YYYY-MM-DD format. ")
    
    # Create task as a dictionary and add to tasks list
    task = {
        "name": task_name,
        "description": task_description,
        "priority": priority,
        "due_date": due_date
    }

    tasks.append(task)
    print(f"\nTask {task_name} added successfully")

    # Save tasks to JSON file after adding
    save_tasks_to_json()


def view_task():
    """Display all tasks in the task list."""
    print("\n====View All Tasks====")

    if not tasks:
        print("No Tasks Found.")
        return
    
    for i, task in enumerate(tasks):
        print(f"\nTask:- #{i + 1}\n")
        print(f"Name: {task['name']}")
        print(f"Description: {task['description']}")
        print(f"Priority: {task['priority']}")
        print(f"Due Date: {task['due_date']}")
        print( "_" * 40)

def update_task():
    """Update and existing task."""
    print(f"\n====Update Task====")

    if not tasks:
        print("No Tasks Found.")
        return

    # Display  tasks for selection
    view_task()

    # Get task index to update
    while True:
        try:
            task_index = int(input("\nEnter the task number to update: "))
            task_index -= 1
            if 0 <= task_index < len(tasks):
                break
            print(f"Please enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("Please enter a valid number.")

    # Get update details
    task = tasks[task_index]
    print(f"\nUpdating Task: {task['name']}")
    print("(Press Enter to keep current value)")

    # Name
    new_name = input(f"Current Name: {task['name']}\nEnter the New Name: ")
    if new_name:
        task['name'] = new_name

    # Description
    new_description = input(f"Current Description: {task['description']}\nEnter New Description: ")
    if new_description:
        task['description'] = new_description

    # Priority
    while True:
        current_priority  = task['priority']
        new_priority = input(f"Current Priority: {current_priority}\nEnter New Priority: ")
        if not new_priority:
            break
        new_priority = new_priority.capitalize()
        if new_priority == "High" or new_priority == "Medium" or new_priority == "Low" :
            task['priority'] = new_priority
            break
        print("Invalid Priority! Enter High , Medium or Low. ")

    # Due Date
    while True:
        current_date = task['due_date']
        new_due_date = input(f"Current Due Date: {current_date}\nEnter Due Date (YYYY-MM-DD): ")
        if not new_due_date:
            break
        if len(new_due_date)==10 and new_due_date[4]== "-" and new_due_date[-3] == "-":
            try:
                year = int(new_due_date[0:4])
                month = int(new_due_date[5:7])
                date = int(new_due_date[8:10])
                if 1 <= month <= 12 and 1 <= date <= 31:
                    task['due_date'] = new_due_date
                    break
            except ValueError:
                pass
        print("Invalid Due Date! Enter valide due date in YYYY-MM-DD format. ")

    print(f"Task #{task_index + 1} updated successfully")

    # Save tasks to JSON file after  updating
    save_tasks_to_json()

def delete_task():
    """Delete a Task from the tasks list."""
    print("\n====Delete Task====")

    if not tasks:
        print("No tasks found.")
        return
    
    # Display tasks for selection
    view_task()

    # Get task index to delete
    while True:
        try:
            task_index = int(input("\nEnter the task number to delete: "))
            task_index -= 1
            if 0 <= task_index < len(tasks):
                break
            print(f"Please enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Confirm deletion
    task_name = tasks[task_index]['name']
    confirm = input(f"Are you sure you want to delete '{task_name}'? (Yes/No): ")

    if confirm.lower() == 'yes':
        delete_task = tasks.pop(task_index)
        print(f"Task '{delete_task['name']}' deleted successfully !")

        # Save tasks to JSON file after  deletion
        save_tasks_to_json()
    else:
        print("Deletion Cancelled")

# JSON file handling functions
def load_tasks_from_json():
    """Load tasks from a JSOn file into the tasks list."""
    try:
        with open("tasks.json","r") as file:
            loaded_tasks = json.load(file)

            # Clear and update the current tasks list
            tasks.clear()
            tasks.extend(loaded_tasks)

            print(f"Successfully loaded {len(tasks)} tasks from JSON file.")
    except FileNotFoundError:
        print("No tasks JSON file found. Starting with an empty task list.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file. Starting with an empty task list.")
    except Exception as e:
        print(f"Error loading tasks: {e}")

def save_tasks_to_json():
    """Save tasks from the tasks list to a JSON file."""
    try:
        with open("tasks.json","w") as file:
            json.dump(tasks, file, indent=4)

            print(f"Successfully saved {len(tasks)} tasks to JSON file.")
    except Exception as e:
        print(f"Error saving tasks: {e}")


def display_menu():
    """Display the Main Menu."""
    print("==== Personal Task Manager ====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

# Test cases for JSON file operations
def run_tests():
    """Rin test cases for JSON functionality."""
    print("\n===== Running Tests =====")

    # Test 1: Save empty task list to JSON 
    print("Test 1: Save empty task list to JSON")
    tasks.clear()
    save_tasks_to_json()

    #Test 2: Load from non-existent file
    print("\nTask 2: Load from non-existent file")
    import os
    if os.path.exists("tasks.json"):
        os.remove("Tasks.json")
    load_tasks_from_json()

    #Test 3: Save and load a task
    print("\nTest 3: Save and load a task")
    task = {
        "name": "Test Task",
        "description": "This is a test task",
        "priority": "Medium",
        "due_date": "2025-04-12"
    }
    tasks.append(task)
    save_tasks_to_json()

    tasks.clear()
    load_tasks_from_json()

    if len(tasks) == 1  and tasks[0]["name"] == "Test Task":
        print("Test passed: Task loaded correctly")
    else:
        print("Test failed: Task not loaded correctly")

    #Test 4: Handle corrupted JSON
    print("\nTest 4: Handle corrupted JSON")
    with open("tasks.json","w") as file:
        file.write("{This is not valid JSON")
    load_tasks_from_json()

    print("\nAll tests completed.")


if __name__ == "__main__":
    # Load tasks from JSON file when the program starts
    load_tasks_from_json()

    # Uncmment the following line to run tests
    # run_tests()
    
    print("Welcome to Personal Task Manager!")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_task()
        elif choice == '3':
            update_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("Exiting the Task Manager.\nGoodbye!")
            break
        else:
            print("Invalid choice!!!.\nplease re-enter a number between 1 to 5.")
