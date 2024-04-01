INSERT INTO Members (fname, lname, age, weight, height, last_payment_date, next_payment_date, next_payment_amnt) VALUES
('Allan', 'Cao', 20, 10, 10, NULL, '2024-04-01', 20),
('Amy', 'Little', 21, 10, 150, NULL, '2024-04-01', 20),
('Audrey', 'Lun', 21, 11, 120, NULL, '2024-04-01', 20),
('Ashley', 'Fong', 20, 9, 9, NULL, '2024-04-01', 20),
('Toph', 'Beifong', 12, 70, 140, '2024-03-01', '2024-04-01', 50);

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
('Hot Yoga Facility'),
('Swimming Pool'),
('Stretching and Mobility'),
('Kick-boxing studio');

INSERT INTO Sessions (trainer_id, room_num, session_time, session_date) VALUES
(1, 1, '12:30:00', '2024-04-5'),
(1, 1, '12:30:00', '2024-04-7'),
(2, 5, '20:00:00', '2024-05-02'),
(2, 8, '19:00:00', '2024-10-30');

INSERT INTO Equipment_Maintenence (condition) VALUES
('GOOD'),
('GOOD'),
('FAIR'),
('Poor'),
('GOOD'),
('GOOD'),
('FAIR'),
('Poor'),
('GOOD'),
('GOOD'),
('FAIR'),
('Repair in Progress');
