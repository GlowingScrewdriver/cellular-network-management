# Database Management System Project 
 
 
## Topic : Cellular network services  
 
 
 
### VIGNESH SINGARAVELU(PES1UG22CS691) 
### VEDANTH PADMARAMAN(PES1UG22CS682) 
 
 
 
 
 
 
 
 
 
# Purpose  
This product implements the Databse sofware server side for managing and keeping track of a cellular network, meant for use by network operators. Operators may host this so ware on their own servers in order to monitor services used by customers. This product handles with high-level aspects of running the cellular network, such as status monitoring, data logging, user interfaces and so on.  
 
# Scope 
 The primary func on of the product is to monitor and control high-level aspects of the cellular network, such as plan and contract selec on, billing, and so on. In addi on to providing an interface for businesses and end users, the so ware also records data useful for analy cs and maintanence, such as usage pa erns, per-tower traffic and status reports and error logs. While the product handles high-level aspects such as the user interface, data collec on and monitoring, it does not deal with the lower-level technological aspects of the cellular network, such as modems, MSCs (mobile switching centres) and cellular towers. It complements cellular network infrastructure in order to ease management and service sale for the operators.  
 
# Description  
 
The server orchestrates the interac on between the cellular network and its users, giving full control to the network operators. Two types of users are recognized: end users and business users. And end user is an individual, iden fied a user ID, who subscribes to the network, by means of one or more phone numbers, for personal use. To aid communica on between the network operators, the user’s e-mail ID and address are collected. Addi onally, for regulatory compliance, a document for the proof of iden ty of the individual is stored; further, the IMEI and ownership of the user’s device(s) are also recorded In order to avail network services, the user buys service plans for his/her phone numbers. Each plan allows calls, SMS messages and Internet access to varying limits, and is priced accordingly. A business user is an en ty that uses the network for commercial purposes. Each business is iden fied by a unique ID and associated with a business name and GSTIN number. Business users avail network services through service contracts. Each contract, iden fied by a unique ID, has a fixed start and end date; other details of the contract are decided in a flexible manner on a per-case basis, unlike with end user service plans. To facilitate health monitoring, the loca on and capacity of each tower maintained by the network operator is stored along with a unique ID. Addi onally, to enable analysis of usage pa erns, usage sta s cs are collected per-device. 
 
 
 
# List of software and tools used : 
-	Python  
-	Tkinter 
-	Mysql 
-	Mysql connector 

# Entity Relationship Diagram 
  ![image](https://github.com/user-attachments/assets/60526f3c-2d3b-42f3-9c82-85ea9028434f)

# Relational Schema
![image](https://github.com/user-attachments/assets/2056f8ed-1a70-47b6-a06a-7faf1bc8bf05)

  
# DDL commands : 
```CREATE DATABASE IF NOT EXISTS cellular_network; 
USE cellular_network; 
 
CREATE TABLE IF NOT EXISTS Device (     device_type ENUM ("smartphone", "featurephone") NOT NULL, 
    IMEI CHAR(15) NOT NULL, 
    PRIMARY KEY (IMEI) 
);
```
 ```
CREATE TABLE IF NOT EXISTS Business_user ( 
    Business_user_ID INT NOT NULL, 
    Business_name VARCHAR(50) NOT NULL, 
    GSTIN CHAR(15) NOT NULL, 
    PRIMARY KEY (Business_user_ID) 
); 
 ```
```
CREATE TABLE IF NOT EXISTS Contract ( 
    Contract_ID INT NOT NULL, 
    Contract_Details INT NOT NULL,     Start_date TIMESTAMP NOT NULL,     end_date TIMESTAMP NOT NULL, 
    Business_user_ID INT NOT NULL, 
    PRIMARY KEY (Contract_ID), 
    FOREIGN KEY (Business_user_ID) REFERENCES 
Business_user(Business_user_ID), 
    CHECK (end_date > Start_date) 
); 
 ```
```
CREATE TABLE IF NOT EXISTS User ( 
    User_name VARCHAR(50) NOT NULL,     User_phone_number CHAR(10) NOT NULL,     apt_name VARCHAR(50) NOT NULL,     street_name VARCHAR(50) NOT NULL,     city VARCHAR(50) NOT NULL,     pincode VARCHAR(6) NOT NULL,     state VARCHAR(50) NOT NULL,     User_Email VARCHAR(100) NOT NULL,     identity_proof INT NOT NULL, 
    IMEI CHAR(15) NOT NULL, 
    PRIMARY KEY (User_phone_number, IMEI), 
    FOREIGN KEY (IMEI) REFERENCES Device(IMEI) 
); 
 ```
```
CREATE TABLE IF NOT EXISTS Towers (     Tower_ID INT NOT NULL, 
    Tower_Location VARCHAR(100) NOT NULL, 
    Tower_Capacity INT NOT NULL, 
    Business_user_ID INT NOT NULL, 
    PRIMARY KEY (Tower_ID), 
    FOREIGN KEY (Business_user_ID) REFERENCES 
Business_user(Business_user_ID), 
    CHECK (Tower_Capacity > 0) 
);
```
 ```
CREATE TABLE IF NOT EXISTS plan_spec ( 
    Plan_ID INT NOT NULL, 
    Plan_name VARCHAR(50) NOT NULL,     Plan_price INT NOT NULL,     data_limit_GB INT NOT NULL,     call_limit INT NOT NULL,     sms_limit INT NOT NULL,     PRIMARY KEY (Plan_ID), 
    CHECK (Plan_price >= 0), 
    CHECK (data_limit_GB >= 0), 
    CHECK (call_limit >= 0), 
    CHECK (sms_limit >= 0) 
); 
 ```
```
CREATE TABLE IF NOT EXISTS User_plan ( 
    Plan_ID INT NOT NULL, 
    IMEI CHAR(15) NOT NULL, 
    User_phone_number CHAR(10) NOT NULL,     date_of_purchase TIMESTAMP NOT NULL, 
    FOREIGN KEY (User_phone_number, IMEI) REFERENCES User(User_phone_number, IMEI), 
    FOREIGN KEY (Plan_ID) REFERENCES plan_spec(Plan_ID) 
);
```
```
CREATE TABLE IF NOT EXISTS uses (     usage_quantum INT NOT NULL,     IMEI CHAR(15) NOT NULL,     Tower_ID INT NOT NULL,     time_stamp TIMESTAMP NOT NULL, 
    PRIMARY KEY (IMEI, Tower_ID), 
    FOREIGN KEY (IMEI) REFERENCES Device(IMEI), 
    FOREIGN KEY (Tower_ID) REFERENCES Towers(Tower_ID), 
    CHECK (usage_quantum >= 0) 
);
```
```
 
CREATE VIEW plan_popularity AS 
    SELECT Plan_ID, COUNT(*) AS user_count 
    FROM User_plan 
    GROUP BY Plan_ID 
    ORDER BY user_count DESC; 
 ```
```
DELIMITER | 
CREATE FUNCTION IF NOT EXISTS tower_load (tower_id INT, period_start 
TIMESTAMP, period_end TIMESTAMP) 
RETURNS DECIMAL(10,2) 
DETERMINISTIC 
BEGIN 
    DECLARE usage_total INT; 
    DECLARE capacity INT; 
     
    SELECT COALESCE(SUM(usage_quantum), 0) 
    INTO usage_total 
    FROM uses     WHERE         uses.Tower_ID = tower_id AND         uses.time_stamp > period_start AND          uses.time_stamp < period_end; 
         
    SELECT Tower_Capacity 
    INTO capacity 
    FROM Towers 
    WHERE Towers.Tower_ID = tower_id; 
     
    IF capacity IS NULL OR capacity = 0 THEN 
        RETURN 0; 
    END IF; 
     
    RETURN CAST(usage_total AS DECIMAL(10,2)) / CAST(capacity AS 
DECIMAL(10,2)); 
END | 
DELIMITER ; 
 ```

 
 
 
 
 
 
 
 
 
# CRUD operations  
 
![image](https://github.com/user-attachments/assets/f594fefd-4907-4bb8-bb7a-a54a39d1a9f2)
![image](https://github.com/user-attachments/assets/34258ee0-5598-4001-8032-8b276662e030)
![image](https://github.com/user-attachments/assets/2f4b2307-5fa9-4062-bab9-5275dadb91fa)
![image](https://github.com/user-attachments/assets/c70a3e28-b262-4a1a-99f6-84fdc1e5f19a)
![image](https://github.com/user-attachments/assets/3ef3153a-48a0-4a39-8856-9281ea751361)
![image](https://github.com/user-attachments/assets/10e2a028-c106-446c-99cc-c8740f6fac9a)



   
# List of functionalities :  

## Register new device 
![image](https://github.com/user-attachments/assets/e769bcee-25e5-4025-9245-ac5ce73c8587)

  
## Register user : 
![image](https://github.com/user-attachments/assets/f79aba5c-3163-47c1-98f5-e32b9c177480)

  
## Purchase a new plan  
![image](https://github.com/user-attachments/assets/3f11048b-70ed-4bcf-a146-ad3c5a8c8d6a)

  
 
## Record Tower Usage 
![image](https://github.com/user-attachments/assets/911cdc4a-b409-4e58-b40c-0cd764cb8938)

  
 
# Triggers : 
## Trigger for preventing tower overload 
```
-- trigger for preventing tower overload 
DELIMITER // 
 
CREATE TRIGGER prevent_tower_overload 
BEFORE INSERT ON uses 
FOR EACH ROW 
BEGIN 
    DECLARE current_load DECIMAL(10,2); 
    DECLARE tower_capacity INT; 
 
    -- Modified query to handle NULL cases with COALESCE     SELECT 
        COALESCE( 
            CAST(COALESCE(SUM(usage_quantum), 0) AS DECIMAL(10,2)) /             NULLIF(CAST(Towers.Tower_Capacity AS DECIMAL(10,2)), 0),             0 
        ) AS current_load, 
        Towers.Tower_Capacity 
    INTO current_load, tower_capacity 
    FROM Towers 
    LEFT JOIN uses ON uses.Tower_ID = Towers.Tower_ID 
    WHERE Towers.Tower_ID = NEW.Tower_ID 
    GROUP BY Towers.Tower_ID, Towers.Tower_Capacity;  
    -- Check if tower exists 
    IF tower_capacity IS NULL THEN 
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Tower does not exist.'; 
    END IF; 
 
    -- Check for overload 
    IF (current_load + CAST(NEW.usage_quantum AS DECIMAL(10,2)) / 
CAST(tower_capacity AS DECIMAL(10,2)) > 1) THEN 
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Tower capacity exceeded, connection denied.'; 
    END IF; 
END // 
```

## Trigger for checking whether a user’s plan is valid or not : 
```
-- Trigger to detect whether the user's plan is valid or not 
DELIMITER | 
CREATE TRIGGER check_plan_validity 
BEFORE INSERT ON uses 
FOR EACH ROW 
BEGIN 
    SELECT COUNT(*) 
    INTO @valid_plans 
    FROM User_plan, plan_spec 
    WHERE 
        User_plan.IMEI = NEW.IMEI and 
        User_plan.Plan_ID = plan_spec.Plan_ID and         DATE_ADD(User_plan.date_of_purchase, INTERVAL plan_spec.validity_days DAY) > NEW.time_stamp; 
 
    IF @valid_plans = 0 THEN 
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'User does not have any valid pack';     END IF; 
END | 
DELIMITER ; 
 ```

# Function :

## Find average load on a tower in a specified period. 
```
-- Function to find load on a given tower in a given time period 
DELIMITER | 
CREATE FUNCTION IF NOT EXISTS tower_load (tower_id INT, period_start 
TIMESTAMP, period_end TIMESTAMP) 
RETURNS DECIMAL(10,2)                     
DETERMINISTIC 
BEGIN 
    DECLARE usage_total INT; 
    DECLARE capacity INT; 
     
    SELECT COALESCE(SUM(usage_quantum), 0)   
    INTO usage_total 
    FROM uses     WHERE 
        uses.Tower_ID = tower_id AND         uses.time_stamp > period_start AND          uses.time_stamp < period_end; 
         
    SELECT Tower_Capacity 
    INTO capacity 
    FROM Towers 
    WHERE Towers.Tower_ID = tower_id; 
     
    IF capacity IS NULL OR capacity = 0 THEN         RETURN 0;                            
    END IF; 
     
    RETURN CAST(usage_total AS DECIMAL(10,2)) / CAST(capacity AS DECIMAL(10,2)); 
END | 
DELIMITER ;
```
 ```
query = "SELECT tower_load(%s, %s, %s) as `load`"
```
invoked using python script 
# Procedure : 

## Fills the null device type to smartphone  

```
DELIMITER $$ 
 
CREATE PROCEDURE UpdateNullDeviceType() 
BEGIN 
    UPDATE Device 
    SET device_type = 'smartphone' 
    WHERE device_type IS NULL; 
END$$ 
 
DELIMITER ;
```
 
```call UpdateNullDeviceType() ```

# Queries

## Q1 : To retrieve plan popularity with names 
```
CREATE VIEW plan_popularity_ AS 
SELECT ps.Plan_name, COUNT(*) as subscribers FROM User_plan up 
JOIN plan_spec ps ON ps.Plan_ID = up.Plan_ID 
GROUP BY ps.Plan_ID, ps.Plan_name 
ORDER BY subscribers DESC; 
 ```
## Q2 : User distribu on across cities 
```
CREATE VIEW user_distribution_ AS 
SELECT city, COUNT(*) as user_count 
FROM User 
GROUP BY city 
ORDER BY user_count DESC;
```
 
## Q3 : Distribu on based on device type 
```
CREATE VIEW device_distribution_ AS 
SELECT device_type, COUNT(*) as device_count 
FROM Device 
GROUP BY device_type
```
 
## Q4 : Average tower capacity by business users  
```
CREATE VIEW avg_tower_capac_bu_ AS 
SELECT bu.Business_name, AVG(t.Tower_Capacity) as avg_capacity 
FROM Towers t 
JOIN Business_user bu ON bu.Business_user_ID = t.Business_user_ID 
GROUP BY bu.Business_user_ID, bu.Business_name;
```
 
 
## Q5 : Currently all the running plans 
```
CREATE VIEW running_plans_ AS 
SELECT up.* 
FROM User_plan up 
JOIN plan_spec ps ON up.Plan_ID = ps.Plan_ID 
WHERE DATE_ADD(up.date_of_purchase, INTERVAL ps.validity_days DAY) > NOW();
```
 
## Q6: Users with mul ple active plans  
```
CREATE VIEW multi_plan_ AS 
SELECT u.User_name, COUNT(DISTINCT up.Plan_ID) as active_plans 
FROM User u 
JOIN User_plan up ON u.IMEI = up.IMEI 
JOIN running_plans_ rp ON up.IMEI = rp.IMEI 
GROUP BY u.User_name 
HAVING active_plans > 1;
```
 
## Q7 : List all users  
```
def list_users(self): 
    """ 
    List all users in the database 
    """ 
    query = "SELECT User_name, User_phone_number FROM User"     try: 
        self.cursor.execute(query)         return self.cursor.fetchall() or {}     except mysql.connector.Error as err: 
        raise Exception(f"Failed to fetch users: {err}") 
 ```
## Q8 : Get user details of a par cular user  
```
def get_user_details(self, phone_number: str) -> Dict[str, Any]: 
    """ 
    Get details of a specific user. 
 
    Args:         phone_number: User's phone number 
    """     try: 
        query = "SELECT * FROM User WHERE User_phone_number = %s"
self.cursor.execute(query, (phone_number,))         return self.cursor.fetchone() or {}     except mysql.connector.Error as err: 
        raise Exception(f"Failed to fetch user details: {err}") 
 
 ```
 
## Q9 : Get user usage for a particular user 
```
def get_user_usage(self, phone_number): 
    """ 
    Get a single user's usage statistics 
    """  
    query = """ 
        SELECT SUM(usage_quantum) AS total_usage, Tower_location 
        FROM uses, User, Towers 
        WHERE 
            User_phone_number = %s 
        GROUP BY Towers.Tower_ID 
    """     try: 
        self.cursor.execute (query, (phone_number,))         return self.cursor.fetchall()     except mysql.connector.Error as err: 
        raise Exception(f"Failed to get usage statistics: {err}") 
 ```
## Q 10 : Retrieves all the idle users  
```
def get_idle_users (self): 
    """ 
    Get users who have no valid plan 
    """     query = """ 
        SELECT User_name, User_Email, t1.IMEI 
        FROM ( 
            SELECT * FROM User_plan 
            EXCEPT 
            SELECT * FROM running_plans_ 
        ) AS t1, User 
        WHERE 
            User.IMEI = t1.IMEI AND 
            User.User_phone_number = t1.User_phone_number 
    """     try:


        self.cursor.execute (query)         return self.cursor.fetchall()     except mysql.connector.Error as err: 
        raise Exception(f"Failed to get usage statistics: {err}") 
 ```
