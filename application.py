#imports
import psycopg2
import datetime
import re
from dateutil.relativedelta import relativedelta

#global variables
loggedin = False
id = ""
MAXGROUP = 8

#getting postgres connection info from user
'''
db = input("Enter database name: ")
pswd = input("Enter password: ")
'''

#making connection
connection = psycopg2.connect(
        dbname="Final Project",
        user="postgres",
        password="Goat1234!!",
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
            print("\t 4. Update Exercise Routine")
            subSelect = validate(1, 4)
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
        print("\t 5. View All Member Profiles")
        print("\t 6. Logout")
        select = validate(1, 6)

        if select == "6":
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

    creditCard = validateCreditCard()

    date = datetime.datetime.now()

    values = "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(fname, lname, weight, height, age, date, 20, creditCard[0], creditCard[1], creditCard[2])

    cursor.execute("INSERT INTO Members (fname, lname, weight, height, age, next_payment_date, payment_amnt, credit_card_num, cvv, name_on_card) " + values)
    connection.commit()
    print("Registration complete. Welcome to the gym!")

def validateCreditCard():
    valid = False
    while valid == False:
        creditCardInput = input("\t Enter your credit card number: ")
        if (re.match("^\d{16}$", creditCardInput) != None):
            creditcardNum = creditCardInput
            valid = True
            break
        print("invalid credit card number")
    valid = False
    while valid == False:
        creditCardInput = input("\t Enter your cvv number: ")
        if (re.search("^\d{3}$", creditCardInput)):
            cvv = creditCardInput
            valid = True
            break
        print("invalid cvv number")
    nameOnCard = input("\t Enter the name on your credit card: ")
    return (creditcardNum, cvv, nameOnCard)

#updating member's personal infomation
def updateInfo():
    global id
    #options
    print("\t1. First name")
    print("\t2. Last name")
    print("\t3. Credit card info")
    option = validate(1, 3)

    if option == "1":
        fname = input("Enter first name: ")
        cursor.execute("UPDATE Members SET fname = %s WHERE member_id = %s", (fname, id))
    elif option == "2":
        lname = input("Enter last name: ")
        cursor.execute("UPDATE Members SET lname = %s WHERE member_id = %s", (lname, id))
    else:
        creditCard = validateCreditCard()
        cursor.execute("UPDATE Members SET credit_card_num = %s, cvv = %s, name_on_card = %s WHERE member_id = %s", (creditCard[0], creditCard[1], creditCard[2], id))
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

#update member's exercise routine
def updateExercise():
    global id

    #options
    print("\t1. Add exercise")
    print("\t2. Delete exercise")
    option = validate(1, 2)

    if option == "1":
        exercise = input("What exercise do you want to add?")
        reps = input("How many reps do want to add")
        cursor.execute("SELECT MAX(exercise_id) FROM Routine WHERE member_id = %s", (id))
        highest_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Routine (exercise_id, member_id, exercise, reps) VALUES (%s, %s, %s, %s)", (highest_id, id, exercise, reps))
        print("Inserted into routine!")
    elif option == "2":
        exercise = input("What is the name of the exercise do you want to delete?")
        cursor.execute(f"DELETE from Routine WHERE member_id = {id} AND exercise = {exercise}")
        if cursor.rowcount == 0:
            print("Exercise not found")
        else:
            print("Deleted Successfully!")

    print("Successfully updated your exercise routine!")

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
        print(" {}\t {}\t\t\t {}".format(data[0], data[1], data[2]))
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
    print("Age\tWeight\t\tHeight")
    for data in dataset:
        print(" {}\t {} lb\t   {} cm".format(data[0], data[1], data[2]))
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
    
    cursor.execute("INSERT INTO Sessions (trainer_id, room_num, session_time, session_date, session_type) VALUES (%s, %s, %s, %s, personal)", (trainer, room, time, date))
    cursor.execute("SELECT session_id FROM Sessions WHERE trainer_id = %s AND room_num = %s AND session_date = %s AND session_time = %s", (trainer, room, date, time))
    sessionId = int((cursor.fetchone())[0])
    print(f"Session sucessfully registered at {date}, {time}")
    cursor.execute("INSERT INTO Takes VALUES (%s,%s)", (id, sessionId))

                
#schedule a group fitness class
def registerForClass():
    cursor.execute("SELECT * FROM Sessions WHERE session_type = 'group'")
    result = cursor.fetchall()
    
    print("Session Id\tRoom #\tDate and Time")
    for r in result:
        print(" {}\t\t {}\t {} @ {}".format(r[0], r[2], r[4], r[3]))

    sessionId = input("Enter the id of the session you would like to sign up for: ")
    cursor.execute("INSERT INTO Takes VALUES (%s, %s)", (id, sessionId))
    print(f"You have successfully been registered for session {sessionId}")


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

def manageTrainerSchedule():
    day = input("Enter what day of the week you're working (Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
    startTime = input("Enter the time you're starting (XX:00): ")
    endTime = input("Enter the time you're finishing (XX:00): ")
    cursor.execute("INSERT INTO Shift (trainer_id, day_of_week, start_time, end_time) VALUES (%s, %s, %s, %s)", (id, day, startTime, endTime))
    print(f"You will be working on {day} from {startTime} to {endTime}")

def displayProfile():

    cursor.execute("SELECT * from Members")
    data = cursor.fetchall()

    print("Member ID\tName")
    for r in data:
        print(" {} \t\t {} {}".format(r[0], r[1], r[2]))
    
    memId = input("What member would you like to check? (member_id): ")

    cursor.execute("SELECT * from Members WHERE member_id = " + memId)
    data = cursor.fetchall()
    print("\nName\t\tLast Payment Date\tNext Payment Date\tPayment Amount")
    print(" {} {}\t {}\t\t{}\t\t ${}".format(data[0][1], data[0][2], data[0][6], data[0][7], data[0][8]))
    displayHealthStats(memId)
    displayGoals("true", memId)
    displayRoutine(memId)

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

def maintenanceMonitoring():
    cursor.execute("SELECT * from Equipment_Maintenence ORDER BY equipment_id ASC")
    result = cursor.fetchall()
    print("Equipment ID\tEquipment Name\t\tCondition")
    for r in result:
        print(" {}\t\t{}\t\t {}".format(r[0], r[1], r[2]))

    ans = str(input("Do you want to update the maintenance (y/n): ")).lower()
    while(ans == "y"):
        while True:
            try:
                equip_id = int(input("What is the equipment's ID: "))
                break
            except ValueError:
                print("Input a number")
        condition = str(input("What is the condition of this piece of equipment (GOOD, FAIR, POOR): "))
        cursor.execute("UPDATE Equipment_Maintenence SET condition = %s WHERE equipment_id = %s", (condition, equip_id))
        print(f"Updated {equip_id} to {condition}")

        ans = str(input("Do you want to update another piece of equipment? (y/n): ")).lower()

def updateClassSchedule():
    date = input("Enter what date you want to schedule your session (Format: YYYY-MM-DD): ")
    time = input("Enter what time you want you want to schedule your session. You can only schedule at XX:00 or XX:30 times (Format: HH:MM): ")

    time = "{}:00".format(time)

    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    time = datetime.datetime.strptime(time, "%H:%M:%S").time()

    trainer = isTrainerAvailable(date,time)
    if(trainer == -1):
        print("No trainer is available at that time, please pick another time")
        return
    
    room = isRoomAvailable(date,time)
       
    if(room == -1):
        print("No room is available at that time, please pick another time")
        return
    
    cursor.execute("INSERT INTO Sessions (trainer_id, room_num, session_type, session_date, session_type) VALUES (%s, %s, %s, %s, group)", (trainer, room, time, date))
    print(f"You are sucessfully registered for a group session at {date}, {time}")

def paymentProcessing():
    cursor.execute("SELECT fname, lname, credit_card_num, payment_amnt FROM Members")
    result = cursor.fetchall()
    print("Full Name\t\tCredit Card #\t\t   Payment Amount")
    for r in result:
        print("{} {}\t\t {}\t    ${}".format(r[0], r[1], r[2], r[3]))
    processPayment = input("\t Confirm payment [y/n]: ")
    if(processPayment == 'y'):
        date = datetime.datetime.now()
        new_date = date + relativedelta(months=1)
        cursor.execute("UPDATE Members SET last_payment_date = %s, next_payment_date = %s", (date, new_date))
        print("Payment Processed.")
    else:
        print("Payment not Processed.")

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
                elif selection == "update4":
                    #update exercise routine
                    print("")
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
                    registerForClass()

            #CALLING TRAINER FUNCTIONS
            elif memType == 2:
                if selection == "1":
                    #schedule management
                    manageTrainerSchedule()
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
                    maintenanceMonitoring()
                elif selection == "3":
                    #update class schedule
                    print("") 
                elif selection == "4":
                    #process billing and payment
                    paymentProcessing()
                elif selection == "5":
                    #view all member profiles
                    cursor.execute("SELECT * from Members")
                    data = cursor.fetchall()

                    print("\nName\t\tLast Payment Date\tNext Payment Date\tPayment Amount")
                    for r in data:
                        print(" {} {}\t {}\t\t{}\t\t ${}".format(r[1], r[2], r[6], r[7], r[8]))

            #commiting changes to postgres
            connection.commit()

    print("Have a nice day :)")  

if __name__=="__main__":
    main()