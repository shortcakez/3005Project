#imports
import psycopg2
import datetime

#global variables
loggedin = False
id = ""

#getting postgres connection info from user
'''
db = input("Enter database name: ")
pswd = input("Enter password: ")
'''

#making connection
connection = psycopg2.connect(
        dbname="project",
        user="postgres",
        password="heyyadora",
        host="localhost",
        port="5432"
    )

#cursor object to run queries
cursor = connection.cursor()

#FUNCTIONS
#Logging in user 
def login():
    global loggedin
    global id

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
        while loggedin == False:
            print("id number invalid, try again")
            id = input("Enter Id: ")
            loggedin = match(memType, id)

    return int(memType)

#checking if id and passwords match
def match(memType, id):
    #determine which table to search
    if memType == "1":
        cursor.execute("SELECT member_id FROM Members")
    elif memType == "2":
        cursor.execute("SELECT trainer_id FROM Trainers")
    else:
        cursor.execute("SELECT staff_id FROM Admin_staff")
    dataset = cursor.fetchall()

    for data in dataset:
        if int(id) == data[0]:
            #match
            print("Logged in! Welcome!")
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
    date = datetime.datetime.now()

    values = "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(fname, lname, weight, height, age, date, 20)
    cursor.execute("INSERT INTO Members (fname, lname, weight, height, age, next_payment_date, next_payment_amnt) " + values)
    connection.commit()
    print("Registration complete. Welcome to the gym!")

#updating member's personal infomation
def updateInfo():
    global id
    #options
    print("\t1. First name")
    print("\t2. Last name")
    option = validate(1, 2)

    if option == "1":
        fname = input("Enter first name: ")
        cursor.execute("UPDATE Members SET fname = %s WHERE member_id = %s", (fname, id))
    else:
        lname = input("Enter last name: ")
        cursor.execute("UPDATE Members SET lname = %s WHERE member_id = %s", (lname, id))

    print("Successfully updated your personal information!")

#update member's fitness goals
def updateGoals():
    global id

    displayGoals("false")
    #options
    print("\t1. Update a goal")
    print("\t2. Add a goal")
    print("\t3. Delete a goal")
    option = validate(1, 3)

    if option == "1": #update goals
        #options
        print("\t1. Update goal statement")
        print("\t2. Change goal to achieved")
        option = validate(1, 3)
        goal_id = input("Enter goal id: ")

        if option == "1":
            goal = input("Enter goal statement: ")
            cursor.execute("UPDATE Fitness_goals SET goal = %s WHERE member_id = %s and goal_id = %s", (goal, id, goal_id))
            print("Successfully updated your goal statement!")
        else:
            cursor.execute("UPDATE Fitness_goals SET achieved = true WHERE member_id = %s and goal_id = %s", (id, goal_id))
            print("Successfully changed goal to achieved!")
    
    elif option == "2": #adding a goal
        goal = input("Enter goal statement: ")
        goal_id = input("Enter goal_id: ") #DON'T KNOW HOW WE GONNA DO THIS...
        values = "VALUES ('{}', '{}', '{}', '{}')".format(goal_id, id, goal, False)
        cursor.execute("INSERT INTO Fitness_goals (goal_id, member_id, goal, achieved) " + values)
        print("Successfully added new goal!")
    else: #deleting a goal
        goal_id = input("Enter goal id: ")
        cursor.execute("DELETE FROM Fitness_goals WHERE member_id = %s and goal_id = %s", ( id, goal_id))
        print("Successfully deleted goal!")

#update member's health metrics
def updateHealth():
    global id

    #options
    print("\t1. Age")
    print("\t2. Height")
    print("\t3. Weight")
    option = validate(1, 3)

    if option == "1":
        age = input("Enter age: ")
        cursor.execute("UPDATE Members SET age = %s WHERE member_id = %s", (age, id))
    elif option == "2":
        height = input("Enter height: ")
        cursor.execute("UPDATE Members SET height = %s WHERE member_id = %s", (height, id))
    else:
        weight = input("Enter weight: ")
        cursor.execute("UPDATE Members SET weight = %s WHERE member_id = %s", (weight, id))

    print("Successfully updated your health metrics!")

#display member's exercise routine
def displayRoutine():
    global id

    cursor.execute("SELECT step, exercise, reps FROM Routine WHERE member_id = " + id)
    dataset = cursor.fetchall()

    print("\nExercise Routine:")
    print("Step\tExercise\t\t\tReps")
    for data in dataset:
        print(" {}\t {}\t\t {}".format(data[0], data[1], data[2]))
    print("\n")

#display member's fitness goals
def displayGoals(achieve):
    global id

    cursor.execute("SELECT goal_id, goal FROM Fitness_goals WHERE achieved = " + achieve + " and member_id = " + id)
    dataset = cursor.fetchall()

    if achieve == "true":
        print("\nFitness Achievements:")
    else:
        print("\nFitness Goals")

    print("goal_id\t  goal")
    for data in dataset:
        print(" {}\t   {}".format(data[0], data[1]))
    print("\n")

#display member's health statistics
def displayHealthStats():
    global id

    cursor.execute("SELECT age, weight, height FROM Members WHERE member_id = " + id)
    dataset = cursor.fetchall()

    print("\nHealth Statistics:")
    print("Age\tWeight\t  Height")
    for data in dataset:
        print(" {}\t {}\t   {}".format(data[0], data[1], data[2]))
    print("\n")

#scheduling a personal training session

        
#schedule a group fitness class


#TRAINER FUNCTIONS


#ADMIN FUNCTIONS



#MAIN
def main():
    memType = 1
    selection = ""
    global loggedin

    while memType != 0:
        #login user
        memType = login()
        while memType != 0:
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
                    updateInfo()
                elif selection == "update2":
                    #update fitness goals
                    updateGoals()
                elif selection == "update3":
                    #update health metrics
                    updateHealth()
                elif selection == "display1":
                    #display exercise routines
                    displayRoutine()
                elif selection == "display2":
                    #display fitness achievements
                    displayGoals("true")
                elif selection == "display3":
                    #display health stats
                    displayHealthStats()
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

if __name__=="__main__":
    main()