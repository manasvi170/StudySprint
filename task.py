
from asyncio import tasks


class TaskManager:
    def __init__(self):
        self.tasks ={}
        self.sno = 0

    def add_task(self):
        self.sno += 1
        print("\nAdding task...")
        task = input(f"Enter task {self.sno}: ").capitalize()
        print(f"\nTask {self.sno} added successfully! ✅")
        self.tasks.update({self.sno: task})


    def display_tasks(self):
        if self.tasks == {}:
            print("\n⚠️ No records available. ⚠️ Enter a task first!")
        else:
            print("\nHere are your tasks 📝")
            for key,value in self.tasks.items():
                print(f"🌷{key}: {value}✨")
            print("\n")

    def delete_task(self,sno):
        if int(sno) in self.tasks:
            del self.tasks[int(sno)]
            print("\nYour task list after deleting the task:")
            self.display_tasks()
            print(f"Successfully deleted task {sno}✅")
        else:
            print(f"\n⚠️Task {sno} not found in your task list⚠️.")


    def edit_tasks(self,sno):
        if sno in self.tasks:
            new_task=input(f"Enter the new task for task number {sno}: ").capitalize()
            self.tasks[sno]=new_task
        else:
            print(f"\n⚠️Task {sno} not found in your task list⚠️.")

