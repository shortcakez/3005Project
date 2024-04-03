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
connection.autocommit=True

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
    
#MEMBER FUNCTIONS
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
#display member's health statistics
#member_id argument is supplied when a trainer want to check a specific member. No argument is when a member is checking themselves
def displayRoutine(member_id = None):
    global id

    if not member_id:
        val = id
    else:
        val = member_id

    cursor.execute("SELECT step, exercise, reps FROM Routine WHERE member_id = " + val)
    dataset = cursor.fetchall()

    print("\nExercise Routine:")
    print("Step\tExercise\t\t\tReps")
    for data in dataset:
        print(" {}\t {}\t\t {}".format(data[0], data[1], data[2]))
    print("\n")

#display member's fitness goals
#display member's health statistics
#member_id argument is supplied when a trainer want to check a specific member. No argument is when a member is checking themselves
def displayGoals(achieve, member_id = None):
    global id

    if not member_id:
        val = id
    else:
        val = member_id

    cursor.execute("SELECT goal_id, goal FROM Fitness_goals WHERE achieved = " + achieve + " and member_id = " + val)
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
#member_id argument is supplied when a trainer want to check a specific member. No argument is when a member is checking themselves
def displayHealthStats(member_id = None):
    global id

    if not member_id:
        val = id
    else:
        val = member_id

    cursor.execute("SELECT age, weight, height FROM Members WHERE member_id = " + val)
    dataset = cursor.fetchall()

    print("\nHealth Statistics:")
    print("Age\tWeight\t  Height")
    for data in dataset:
        print(" {}\t {}\t   {}".format(data[0], data[1], data[2]))
    print("\n")

#scheduling a personal training session
def schedulePT():

    date = input("Enter what date you want to schedule your session (Format: YYYY-MM-DD): ")
    time = input("Enter what time you want you want to schedule your session. You can only schedule at XX:00 or XX:30 times (Format: HH:MM): ")

    time = "{}:00".format(time)

    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    time = datetime.datetime.strptime(time, "%H:%M:%S").time()

    trainer = isTrainerAvailable(date,time)
    if(trainer == -1):
        print("No trainer is available at that time, please pick another time")
        return
    
    #We found a trainer 

    room = isRoomAvailable(date,time)
       
    if(room == -1):
        print("No trainer is available at that time, please pick another time")
        return
    
    cursor.execute("INSERT INTO Sessions (trainer_id, room_num, session_time, session_date) VALUES (%s, %s, %s, %s)", (trainer, room, time, date))
    print(f"Session sucessfully registered at {date}, {time}")
                
#schedule a group fitness class


#TRAINER FUNCTIONS
def viewTrainerSchedule(trainer_id):
    cursor.execute("SELECT * from Sessions WHERE trainer_id = " + str(trainer_id))
    return cursor.fetchall()

def isTrainerAvailable(date, time) -> int:
    cursor.execute("SELECT COUNT(*) FROM TRAINERS;")
    trainer_num = cursor.fetchone()[0] # gets the number of trainers

    for i in range(1,trainer_num+1):

        schedule = viewTrainerSchedule(i)
        trainer_free = True
        for row in schedule:
            if row[3] == time and row[4] == date:
                trainer_free = False
                break
        
        if trainer_free == False:
            continue

        return i
    
    # if still not returned, then no trainer is available
    return -1

def displayProfile():

    cursor.execute("SELECT * from Members")
    data = cursor.fetchall()

    for r in data:
        print("member_id: {} full Name: {} {}".format(r[0], r[1], r[2]))
    
    id = input("What member would you like to check? (member_id): ")

    cursor.execute("SELECT * from Members WHERE member_id = " + id)
    data = cursor.fetchall()
    print("")
    for r in data:
        print("member_id: {} full Name: {} {} age: {} weight: {} height: {} last_payment_date: {} next_payment_date: {} next_payment_amnt: {}".format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))
    displayHealthStats(id)
    displayGoals("true", id)
    displayRoutine(id)

#ADMIN FUNCTIONS
def viewRoomsSchedule(num):
    cursor.execute("SELECT * from Sessions WHERE room_num = " + str(num))
    return cursor.fetchall()

def isRoomAvailable(date, time)->int:
    cursor.execute("SELECT COUNT(*) FROM Rooms;")
    room_num = cursor.fetchone()[0] # gets the number of rooms

    for j in range(1,room_num+1):
        room_schedule = viewRoomsSchedule(j)
        room_free = True
        for row in room_schedule:
            if row[3] == time and row[4] == date: 
                room_free = False
                break
    
        if room_free == False:
            continue
        return j

    # if still not returned, then no room is available
    return -1

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
                    schedulePT()
                    #schedule personal training session
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
                    displayProfile()

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