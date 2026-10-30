from task import TaskManager

print("Welcome to the StudySprint!")

name = input("What's your name? ").capitalize()
print(f"\nHello, {name}! Let's get productive.🎧☕💻✨\n")

work = TaskManager()

while True:
    print("\nHere are some options...\n\t\t\t🌿•₊✧💻⋆⭒˚☕️｡⋆")
    print("Add a new task? (Press 1)\nDisplay Tasks? (Press 2)\nEdit Task? (Press 3)\nCompleted/Delete Task? (Press 4)\nExit? (Press 0)")
    options = input("\nEnter your choice: ")

    if options == "1":   #Add tasks
        work.add_task()

    elif options=="2":   #Display current tasks
        work.display_tasks()

    elif options=="3":   #Edit`s task
        work.display_tasks()
        task_number=input(f"\nEnter the task number you want to edit: ")
        work.edit_tasks(int(task_number))

    elif options=="4":    #Delete`s task
        print("\nCurrent task list:")
        work.display_tasks()
        task_number=input("Which task would you like to delete? (Enter the task number): ")
        work.delete_task(task_number)


    elif options=="0":   #Exit the program
        print(f"\nThank you for using StudySprint, {name}! Have a productive day౨ৎ 📖☕🎧🤍")
        break
        


