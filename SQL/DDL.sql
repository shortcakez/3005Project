DROP TABLE IF EXISTS Members, Fitness_goals, Routine, Trainers, Rooms, Sessions, Admin_staff, Equipment_Maintenence, Takes, Shift;

CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    age SMALLINT NOT NULL,
    weight FLOAT,
    height FLOAT,
    last_payment_date DATE,
    next_payment_date DATE,
    payment_amnt FLOAT,
    credit_card_num VARCHAR(16) UNIQUE NOT NULL,
    cvv VARCHAR(3) NOT NULL,
    name_on_card VARCHAR(30) NOT NULL
);

CREATE TABLE Fitness_goals (
    goal_id INT,
    member_id INT, 
    goal VARCHAR(255) NOT NULL,
    achieved BOOLEAN,
    PRIMARY KEY (member_id, goal_id),
    FOREIGN KEY (member_id) REFERENCES Members (member_id)
);

CREATE TABLE Routine (
    exercise_id SERIAL PRIMARY KEY,
    member_id INT,
    exercise VARCHAR(50) NOT NULL,
    reps INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES Members (member_id)
);

CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL
);

CREATE TABLE Shift (
    shift_id SERIAL PRIMARY KEY,
    trainer_id int,
    day_of_week VARCHAR(3) NOT NULL,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (trainer_id)
        REFERENCES Trainers (trainer_id)
);

CREATE TABLE Rooms (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50),
    availability BOOLEAN
);

CREATE TABLE Sessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT,
    room_num INT,
    session_time TIME,
    session_date DATE,
    session_type VARCHAR(10),
    FOREIGN KEY (trainer_id)
        REFERENCES Trainers (trainer_id),
    FOREIGN KEY (room_num)
        REFERENCES Rooms (room_id)
);

CREATE TABLE Admin_staff (
    staff_id SERIAL PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL
);

CREATE TABLE Equipment_Maintenence (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(30),
    condition VARCHAR(30)
);

CREATE TABLE Takes (
    member_id INT,
    session_id INT,
    FOREIGN KEY (member_id)
        REFERENCES Members (member_id),
    FOREIGN KEY (session_id)
        REFERENCES Sessions (session_id)
);
