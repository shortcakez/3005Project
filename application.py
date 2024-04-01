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
#Logging in user 
def login():
    print("LOGIN")
    print("select one of the following options (# only):\n\t 1. Gym member\n\t 2. Trainer\n\t 3. Admin\n\t 4. New gym member\n\t 5. Quit")

    while loggedin == False:
        #which type of member are they
        memType = validate(1, 6)

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
        cursor.execute("SELECT id, password FROM Members")
    elif memType == 2:
        cursor.execute("SELECT id, password FROM Trainers")
    else:
        cursor.execute("SELECT id, password FROM Admin_staff")
    dataset = cursor.fetchall()

    for data in dataset:
        if id == data[0]:
            #match
            return True
    
    #no match
    return False

#display menu and get user input for what they want to do
def menu(memType):
    print("\nSelect one of the following options (# only):")
    if memType == 1: #display member options
        #main options
        print("\t 1. Profile Management")
        print("\t 2. Display Dashboard")
        print("\t 3. Manage Schedule")
        print("\t 4. Logout")
        select = validate(1, 4)

        #sub options
        if select == "1":
            print("\t 1. Update personal information")
            print("\t 2. Update fitness goals")
            print("\t 3. Update health metrics")
            subSelect = validate(1, 3)
            return "update" + subSelect
        elif select == "2":
            print("\t 1. Display exercise routines")
            print("\t 2. Display fitness acheivements")
            print("\t 3. Display health statistics")
            subSelect = validate(1, 3)
            return "display" + subSelect
        elif select == "3":
            print("\t 1. Schedule personal training session")
            print("\t 2. Schedule group fitness class")
            subSelect = validate(1, 2)
            return "schedule" + subSelect
        elif select == "4":
            print("LOGGING OUT")
            return "0"

    elif memType == 2: #dipslay trainer options
        #main options
        print("\t 1. Manage Schedule")
        print("\t 2. View Member Profile")
        print("\t 3. Logout")
        select = validate(1, 3)

        if select == "3":
            print("LOGGING OUT")
            return "0"

        return select
    
    else: #display admin options
        #main options
        print("\t 1. Manage Room Bookings")
        print("\t 2. Monitor Equipement Maintainence")
        print("\t 3. Update Class Schedule")
        print("\t 4. Process Billing and Payment")
        print("\t 5. Logout")
        select = validate(1, 5)

        if select == "5":
            print("LOGGING OUT")
            return "0"

        return select

#ensures that the user input is a valid option, otherwise, it'll keep asking user for input
def validate(min, max):
    select = input(">> ")
    while int(select) < min or int(select) > max:
            print("invalid option, try again")
            select = input(">> ")
    return select
    
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
    connection.commit()
    print("Registration complete. Welcome to the gym!")

#TRAINER FUNCTIONS


#ADMIN FUNCTIONS



memType = 1
selection = ""

while memType != 0:
    #login user
    memType = login()
    while loggedin == True:
        #displaying menu options and getting user selection
        selection = menu(memType)

        #logging out to login menu
        if selection == "0":
            loggedin = False
            break

        #allocating what function to call
        #CALLING MEMBER FUNCTIONS
        if memType == 1: 
            if selection == "update1":
                #update personal info
                print("")
            elif selection == "update2":
                #update fitness goals
                print("")
            elif selection == "update3":
                #update health metrics
                print("")
            elif selection == "display1":
                #display exercise routines
                print("")
            elif selection == "display2":
                #display fitness achievements
                print("")
            elif selection == "display3":
                #display health stats
                print("")
            elif selection == "schedule1":
                #schedule personal training session
                print("")
            elif selection == "schedule2":
                #schedule group fitness class
                print("")

        #CALLING TRAINER FUNCTIONS
        elif memType == 2:
            if selection == "1":
                #schedule management
                print("")
            elif selection == "2":
                #view member profile
                print("")

        #CALLING ADMIN FUNCTIONS
        elif memType == 3: 
            if selection == "1":
                #manage room booking
                print("")
            elif selection == "2":
                #monitor eqipement
                print("")
            elif selection == "3":
                #update class schedule
                print("") 
            elif selection == "4":
                #process billing and payment
                print("")

        #commiting changes to postgres
        connection.commit()

print("Have a nice day :)")  