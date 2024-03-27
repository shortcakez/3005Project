#imports
import psycopg2

#global variables
loggedin = False

#getting postgres connection info from user
db = input("Enter database name: ")
username = input("Enter user name: ")
pswd = input("Enter password: ")

#making connection
connection = psycopg2.connect(
        dbname=db,
        user=username,
        password=pswd,
        host="localhost",
        port="5432"
    )

#cursor object to run queries
cursor = connection.cursor()

#FUNCTIONS
#decide what to display depending on who logs in
def login():
    print("LOGIN")
    print("select one of the following options (# only):\n\t 1. Gym member\n\t 2. Trainer\n\t 3. Admin\n\t 4. New gym member\n\t 5. Quit")

    while loggedin == False:
        #which type of member are they
        memType = input(">> ")
        while int(memType) < 1 or int(memType) > 6:
            print("invalid option, try again")
            memType = input(">> ")

        #if they are a new member registering
        if memType == "4":
            userRegistration()
            return 1
        
        #quitting application
        if memType == "5":
            return 0

        #getting user id
        id = input("Enter Id: ")
        loggedin = match(memType, id)
        if loggedin == False:
            print("id number invalid, try again")

    return int(memType)

#checking if id and passwords match
def match(memType, id):
    #determine which table to search
    if memType == 1:
        cursor.execute("SELECT id, password FROM members")
    elif memType == 2:
        cursor.execute("SELECT id, password FROM trainers")
    else:
        cursor.execute("SELECT id, password FROM admins")

    dataset = cursor.fetchall()
    matched = False
    for data in dataset:
        if id == data[0]:
            matched = True
            break
    
    return matched

#display menu
def menu(memType):
    print("\nSelect one of the following options (# only):")
    if memType == 1: #display member options
        #main options
        print("\t 1. Profile Management")
        print("\t 2. Display Dashboard")
        print("\t 3. Manage Schedule")
        print("\t 4. Logout")
        select = input(">> ")

        #sub options
        if select == "1":
            print("\t 1. Update personal information")
            print("\t 2. Update fitness goals")
            print("\t 3. Update health metrics")
            subSelect = input(">> ")
            return "update" + subSelect
        elif select == "2":
            print("\t 1. Display exercise routines")
            print("\t 2. Display fitness acheivements")
            print("\t 3. Display health statistics")
            subSelect = input(">> ")
            return "display" + subSelect
        elif select == "3":
            print("\t 1. Schedule personal training session")
            print("\t 2. Schedule group fitness class")
            subSelect = input(">> ")
            return "schedule" + subSelect
        elif select == "4":
            print("LOGGING OUT")
            return "0"

    elif memType == 2: #dipslay trainer options
        print("")
    else: #display admin options
        print("")

    
#MEMEBER FUNCTIONS
#add new user
def userRegistration():
    #get user input
    print("Registation:")
    fname = input("\t Enter first name: ")
    lname = input("\t Enter last name: ")
    age = input("\t Enter your age: ")
    weight = input("\t Enter your weight (lb): ")
    height = input("\t Enter your height (cm): ")

    values = "VALUES ('{}', '{}', '{}', '{}')".format(fname, lname, weight, height, age)
    cursor.execute("INSERT INTO students (fname, lname, weight, height, age) " + values)
    print("Registration complete. Welcome to the gym!")

#TRAINER FUNCTIONS


#ADMIN FUNCTIONS


#APPLICATION SET UP
#login user
memType = login()

while memType != 0:
    #display menu options
    select = menu(memType)

    #executing based off input
    while select != "0":
        if memType == 1:
            if select == "update1":
                #function
                print("")
        elif memType == 2:
            if select == "":
                #function
                print("")
        elif memType == 3:
            if select == "":
                #function
                print("")
        select = menu(memType)
    
    