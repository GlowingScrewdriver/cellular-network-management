use cellular_network;

-- Add devices
INSERT INTO Device (device_type, IMEI) VALUES
    ('smartphone', '123456789012345'),
    ('smartphone', '234567890123456'),
    ('featurephone', '345678901234567'),
    ('smartphone', '456789012345678'),
    ('smartphone', '567890123456789'),
    ('featurephone', '678901234567890'),
    ('smartphone', '789012345678901'),
    ('smartphone', '890123456789012'),
    ('featurephone', '901234567890123'),
    ('smartphone', '012345678901234');

-- Add business users
INSERT INTO Business_user (Business_user_ID, Business_name, GSTIN) VALUES
    (1, 'Zara Fashion Ltd', '29AADCU9604R1ZJ'),
    (2, 'Levi Strauss India Pvt Ltd', '27AADCU9604R1ZJ'),
    (3, 'McDonalds India Pvt Ltd', '33AADCU9604R1ZJ'),
    (4, 'H&M India Pvt Ltd', '22AADCU9604R1ZJ');

-- Add contracts for business users
INSERT INTO Contract (Contract_ID, Contract_Details, Start_date, end_date, Business_user_ID) VALUES
    (1, 1001, '2023-01-01 00:00:00', '2024-12-31 23:59:59', 1),
    (2, 1002, '2023-02-01 00:00:00', '2024-12-31 23:59:59', 1),
    (3, 2001, '2023-01-15 00:00:00', '2024-12-31 23:59:59', 2),
    (4, 3001, '2023-03-01 00:00:00', '2024-12-31 23:59:59', 3),
    (5, 4001, '2023-04-01 00:00:00', '2024-12-31 23:59:59', 4);

-- Add towers
INSERT INTO Towers (Tower_ID, Tower_Location, Tower_Capacity, Business_user_ID) VALUES
    (1, 'Mumbai West', 1000, 1),
    (2, 'Mumbai East', 1200, 1),
    (3, 'Delhi North', 1500, 2),
    (4, 'Delhi South', 1300, 2),
    (5, 'Bangalore', 1400, 3),
    (6, 'Chennai', 1100, 3),
    (7, 'Kolkata', 1000, 4),
    (8, 'Hyderabad', 1200, 4);

-- Add users
INSERT INTO User (User_name, User_phone_number, apt_name, street_name, city, pincode, state, User_Email, identity_proof, IMEI) VALUES
    ('Rahul Kumar', '9876543210', 'Green Park', 'MG Road', 'Mumbai', '400001', 'Maharashtra', 'rahul@email.com', 12345, '123456789012345'),
    ('Priya Singh', '9876543211', 'Blue Bells', 'Park St', 'Delhi', '110001', 'Delhi', 'priya@email.com', 12346, '234567890123456'),
    ('Amit Patel', '9876543212', 'Sea View', 'Marine Dr', 'Mumbai', '400002', 'Maharashtra', 'amit@email.com', 12347, '345678901234567'),
    ('Deepa Gupta', '9876543213', 'Sky Tower', 'Ring Road', 'Bangalore', '560001', 'Karnataka', 'deepa@email.com', 12348, '456789012345678'),
    ('Suresh Reddy', '9876543214', 'Palm Grove', 'Anna Salai', 'Chennai', '600001', 'Tamil Nadu', 'suresh@email.com', 12349, '567890123456789'),
    ('Meera Iyer', '9876543215', 'River View', 'MG Road', 'Bangalore', '560002', 'Karnataka', 'meera@email.com', 12350, '678901234567890'),
    ('Rajesh Shah', '9876543216', 'Sun City', 'SV Road', 'Mumbai', '400003', 'Maharashtra', 'rajesh@email.com', 12351, '789012345678901'),
    ('Anita Sharma', '9876543217', 'Moon Tower', 'CP', 'Delhi', '110002', 'Delhi', 'anita@email.com', 12352, '890123456789012');

-- Add plan specifications
INSERT INTO plan_spec VALUES
    (1, "Balanced", 200, 10, 80, 200, 60),
    (2, "Entertainment", 300, 40, 60, 60, 80),
    (3, "Talktime Add-on", 50, 0, 100, 0, 40),
    (4, "Data Add-on", 50, 10, 0, 0, 30);

-- Add user plans (subscriptions)
INSERT INTO User_plan (Plan_ID, IMEI, User_phone_number, date_of_purchase) VALUES
    (1, '123456789012345', '9876543210', '2024-10-15 10:00:00'),
    (2, '234567890123456', '9876543211', '2024-11-11 11:00:00'),
    (1, '345678901234567', '9876543212', '2024-10-17 12:00:00'),
    (2, '456789012345678', '9876543213', '2024-09-18 13:00:00'),
    (3, '123456789012345', '9876543210', '2024-11-12 14:00:00'),
    (4, '567890123456789', '9876543214', '2024-10-20 15:00:00'),
    (1, '678901234567890', '9876543215', '2023-11-13 16:00:00'),
    (2, '789012345678901', '9876543216', '2023-09-22 17:00:00'),
    (3, '890123456789012', '9876543217', '2024-10-23 18:00:00');

-- Add usage data
INSERT INTO uses (usage_quantum, IMEI, Tower_ID, time_stamp) VALUES
    (100, '123456789012345', 1, '2024-10-15 10:30:00'),
    (150, '234567890123456', 3, '2024-10-16 11:30:00'),
    (200, '345678901234567', 2, '2024-10-17 12:30:00'),
    (350, '456789012345678', 5, '2024-10-18 13:30:00'),
    (200, '567890123456789', 6, '2024-10-20 15:30:00'),
    (250, '890123456789012', 3, '2024-10-23 18:30:00'),
    (400, '123456789012345', 2, '2024-11-15 10:30:00'),
    (350, '234567890123456', 4, '2024-11-16 11:30:00'),
    (450, '345678901234567', 1, '2024-11-17 12:30:00'),
    (500, '456789012345678', 6, '2024-11-18 13:30:00');


