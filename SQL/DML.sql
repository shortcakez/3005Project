INSERT INTO Members (fname, lname, age, weight, height, last_payment_date, next_payment_date, next_payment_amnt, credit_card_num, cvv, name_on_card) VALUES
('Allan', 'Cao', 20, 10, 10, NULL, '2024-04-01', 20, '1234123412341234', '123', 'Allan Cao'),
('Amy', 'Little', 21, 10, 150, NULL, '2024-04-01', 20, '2345234523452345', '234', 'Amy Little'),
('Audrey', 'Lun', 21, 11, 120, NULL, '2024-04-01', 20, '3456345634563456', '345', 'Audrey Lun'),
('Ashley', 'Fong', 20, 9, 9, NULL, '2024-04-01', 20, '4567456745674567', '456', 'Ashley Fong'),
('Toph', 'Beifong', 12, 70, 140, '2024-03-01', '2024-04-01', 20, '5678567856785678', '567', 'Toph Beifong');

INSERT INTO Trainers (fname, lname) VALUES
('Jeremy', 'Gilbert'),
('Hannah', 'Montana');

INSERT INTO Admin_Staff (fname, lname) VALUES
('Lucy', 'Wang'),
('Vivian', 'Ngan');

INSERT INTO Fitness_goals (goal_id, member_id, goal, achieved) VALUES
(1, 1, 'Bench 175', false),
(2, 1, 'Bench 145', true),
(1, 2, 'Run 5k', false),
(2, 2, 'Do 5 pushups', false),
(1, 3, 'Run a half-marathon', false),
(2, 3, 'Do 50 jumping jacks', true),
(1, 4, 'Do a 3-pointer', true),
(2, 4, 'Run 10k', false),
(1, 5, 'Learn sandbending', false),
(2, 5, 'Fight firelord Ozai', true),
(3, 5, 'Bench Ba Sing Se', false);

INSERT INTO Routine (step, member_id, exercise, reps) VALUES
(1, 1, 'Bicep Curl 20lbs', 20),
(2, 1, 'Bicep Curl 50lbs', 30),
(3, 1, 'Bench 140', 10),
(1, 2, 'Sprint 100m', 5),
(2, 2, 'Pull-ups', 3),
(1, 3, 'Run a quarter-marathon', 2),
(2, 3, 'Run a third-marathon', 1),
(1, 4, 'Forward lunge', 50),
(2, 4, 'Sideways lunge', 50),
(1, 5, 'Throw boulder at Aang', 10),
(2, 5, 'Use seismic sense', 30),
(3, 5, 'Beat THE Boulder', 5);

INSERT INTO Rooms (room_type) VALUES
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room'),
('Weight Room');

INSERT INTO Sessions (trainer_id, room_num, session_time, session_date) VALUES
(1, 1, '12:30:00', '2024-04-5'),
(1, 1, '12:30:00', '2024-04-7'),
(2, 5, '20:00:00', '2024-05-02'),
(2, 8, '19:00:00', '2024-10-30');

INSERT INTO Equipment_Maintenence (equipment_id, equipment_name, condition) VALUES
(1, 'Bench_Press','GOOD'),
(2, 'Leg_Press', 'GOOD'),
(3, 'Pulldown_Machine','FAIR'),
(4, 'Arm_Curl_Machine','Poor'),
(5, 'Squat_Rack','GOOD'),
(6, 'Treadmill', 'GOOD'),
(7, 'Pull_Up_Machine','FAIR'),
(8, 'Shoulder_Press','Poor'),
(9, 'Leg_Curl_Machine', 'GOOD'),
(10, 'Exercise_Bike', 'GOOD'),
(11, 'Stair_Machine','FAIR'),
(12, 'Chest_Press', 'Repair in Progress');


INSERT INTO Shift (trainer_id, day_of_week, start_time, end_time) VALUES
(1, "Mon", "09:00:00", "05:00:00"),
(1, "Tue", "09:00:00", "05:00:00"),
(1, "Wed", "09:00:00", "05:00:00"),
(1, "Thu", "11:00:00", "07:00:00"),
(1, "Fri", "09:00:00", "05:00:00"),
(1, "Sun", "09:00:00", "05:00:00"),
(2, "Mon", "12:00:00", "08:00:00"),
(2, "Tue", "09:00:00", "05:00:00"),
(2, "Wed", "09:00:00", "05:00:00"),
(2, "Fri", "12:00:00", "08:00:00"),
(2, "Sat", "09:00:00", "05:00:00")
