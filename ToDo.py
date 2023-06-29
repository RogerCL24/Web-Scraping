import os 

runProgram = True
todolist = []

# Show the menu with the options of the ToDo list
def showMenuOptions():
    print("")
    print("")
    print("Please select an option: ")
    print("")
    print("")
    print("1. Create a task")
    print("2. Mark a task as completed")
    print("3. Erase a task")
    print("4. Show list")
    print("5. Leave")
# Delete a task of the ToDo list
def deleteTask():
    os.system("clear")
    print("--------Erase a task--------")
    global todolist
    showToDoList()
    taskID = int(input("Type the task you want to delete please: "))
    del todolist[taskID - 1]
    showToDoList()

#Mark a task as completed
def updateTask():
    os.system("clear")
    print("--------Update a task as done--------")
    global todolist
    if len(todolist) == 0:
        print("Sorry, you do not have any task to update")
    else:    
        showToDoList()
        task = int(input("Type the task number you have completed please: "))
        if task <= len(todolist):
            todolist[task - 1] = todolist[task - 1] + " ✅"
            os.system("clear") 
            showToDoList()
        else:
            updateTask()

#Add a new task to the ToDo list and show what you have added
def createTask():
    os.system("clear")
    print("--------Create a task--------")
    global todolist
    task = input("Please write the name of the task: ")
    todolist.append(task)
    showToDoList()

# Show the current ToDo list
def showToDoList():
    global todolist
    print()
    print()
    print("***********************************")
    for i in todolist:
        print(f"{todolist.index(i) + 1}. {i}")
    print("***********************************")
    print()
    print()

def main():
    global runProgram
    print("./: WELCOME TO MY PYTHON TO-DO LIST :\.")

    while runProgram:
        showMenuOptions()
        opt = int(input("Type the option number: "))

        if opt == 1:
            createTask()
        elif opt == 2:
            updateTask()
        elif opt == 3:
            deleteTask()
        elif opt == 4:
            showToDoList()
        elif opt == 5:
            print("Leaving...")
            runProgram = False
        else:
            print("Wrong option, try again please")


if __name__ == "__main__":
    main()