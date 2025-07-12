# Author: Riyas
# Date: 4th Mar 2025

# Stage 1 : List-Based Design and Basic CRUD Operations

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
    
    # Create task as a list and add to tasks
    task = [task_name, task_description, priority, due_date]
    tasks.append(task)
    print(f"\nTask {task_name} added successfully")

def view_task():
    """Display all tasks in the task list."""
    print("\n====View All Tasks====")

    if not tasks:
        print("No Tasks Found.")
        return
    
    for i, task in enumerate(tasks):
        print(f"\nTask:- #{i + 1}\n")
        print(f"Name: {task[0]}")
        print(f"Description: {task[1]}")
        print(f"Priority: {task[2]}")
        print(f"Due Date: {task[3]}")
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
    print(f"\nUpdating Task: {tasks[task_index][0]}")
    print("(Press Enter to keep current value)")

    # Name
    new_name = input(f"Current Name: {tasks[task_index][0]}\nEnter the New Name: ")
    if new_name:
        tasks[task_index][0] = new_name

    # Description
    new_description = input(f"Current Description: {tasks[task_index][1]}\nEnter New Description: ")
    if new_description:
        tasks[task_index][1] = new_description

    # Priority
    while True:
        new_priority = input(f"Current Priority: {tasks[task_index][2]}\nEnter New Priority: ")
        if not new_priority:
            break
        new_priority = new_priority.capitalize()
        if new_priority == "High" or new_priority == "Medium" or new_priority == "Low" :
            tasks[task_index][2] = new_priority
            break
        print("Invalid Priority! Enter High , Medium or Low. ")

    # Due Date
    while True:
        new_due_date = input(f"Current Due Date: {tasks[task_index][3]}\nEnter Due Date (YYYY-MM-DD): ")
        if not new_due_date:
            break
        if len(new_due_date)==10 and new_due_date[4]== "-" and new_due_date[-3] == "-":
            try:
                year = int(new_due_date[0:4])
                month = int(new_due_date[5:7])
                date = int(new_due_date[8:10])
                if 1 <= month <= 12 and 1 <= date <= 31:
                    tasks[task_index][3] = new_due_date
                    break
            except ValueError:
                pass
        print("Invalid Due Date! Enter valide due date in YYYY-MM-DD format. ")

    print(f"Task #{task_index + 1} updated successfully")

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
    task_name = tasks[task_index][0]
    confirm = input(f"Are you sure you want to delete '{task_name}'? (Yes/No): ")

    if confirm.lower() == 'yes':
        delete_task = tasks.pop(task_index)
        print(f"Task '{delete_task[0]}' deleted successfully !")
    else:
        print("Deletion Cancelled")

def display_menu():
    """Display the Main Menu."""
    print("==== Personal Task Manager ====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

if __name__ == "__main__":
    # Main function called to test CRUD
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