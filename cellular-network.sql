CREATE DATABASE IF NOT EXISTS cellular_network;
USE cellular_network;

CREATE TABLE IF NOT EXISTS Device (
    device_type ENUM ("smartphone", "featurephone") NOT NULL,
    IMEI CHAR(15) NOT NULL,
    PRIMARY KEY (IMEI)
);

CREATE TABLE IF NOT EXISTS Business_user (
    Business_user_ID INT NOT NULL,
    Business_name VARCHAR(50) NOT NULL,  -- Increased length for business names
    GSTIN CHAR(15) NOT NULL,            -- Changed to 15 chars as per standard GSTIN length
    PRIMARY KEY (Business_user_ID)
);

CREATE TABLE IF NOT EXISTS Contract (
    Contract_ID INT NOT NULL,
    Contract_Details INT NOT NULL,
    Start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    Business_user_ID INT NOT NULL,
    PRIMARY KEY (Contract_ID),
    FOREIGN KEY (Business_user_ID) REFERENCES Business_user(Business_user_ID),
    CHECK (end_date > Start_date)       -- Added constraint to ensure valid dates
);

CREATE TABLE IF NOT EXISTS User (
    User_name VARCHAR(50) NOT NULL,      -- Increased length for names
    User_phone_number CHAR(10) NOT NULL,
    apt_name VARCHAR(50) NOT NULL,       -- Increased for longer apartment names
    street_name VARCHAR(50) NOT NULL,    -- Increased for longer street names
    city VARCHAR(50) NOT NULL,           -- Increased for longer city names
    pincode VARCHAR(6) NOT NULL,
    state VARCHAR(50) NOT NULL,          -- Increased for longer state names
    User_Email VARCHAR(100) NOT NULL,    -- Increased for longer email addresses
    identity_proof INT NOT NULL,
    IMEI CHAR(15) NOT NULL,
    PRIMARY KEY (User_phone_number, IMEI),
    FOREIGN KEY (IMEI) REFERENCES Device(IMEI)
);

CREATE TABLE IF NOT EXISTS Towers (
    Tower_ID INT NOT NULL,
    Tower_Location VARCHAR(100) NOT NULL, -- Increased for detailed locations
    Tower_Capacity INT NOT NULL,
    Business_user_ID INT NOT NULL,
    PRIMARY KEY (Tower_ID),
    FOREIGN KEY (Business_user_ID) REFERENCES Business_user(Business_user_ID),
    CHECK (Tower_Capacity > 0)           -- Added constraint for valid capacity
);

CREATE TABLE IF NOT EXISTS plan_spec (
    Plan_ID INT NOT NULL,
    Plan_name VARCHAR(50) NOT NULL,      -- Increased for longer plan names
    Plan_price INT NOT NULL,
    data_limit_GB INT NOT NULL,
    call_limit INT NOT NULL,
    sms_limit INT NOT NULL,
    validity_days INT NOT NULL,
    PRIMARY KEY (Plan_ID),
    CHECK (Plan_price >= 0),             -- Added constraints for valid values
    CHECK (data_limit_GB >= 0),
    CHECK (call_limit >= 0),
    CHECK (sms_limit >= 0)
);

CREATE TABLE IF NOT EXISTS User_plan (
    Plan_ID INT NOT NULL,
    IMEI CHAR(15) NOT NULL,
    User_phone_number CHAR(10) NOT NULL,
    date_of_purchase TIMESTAMP NOT NULL,
    PRIMARY KEY (Plan_ID, IMEI, date_of_purchase),  -- Added composite primary key
    FOREIGN KEY (User_phone_number, IMEI) REFERENCES User(User_phone_number, IMEI),
    FOREIGN KEY (Plan_ID) REFERENCES plan_spec(Plan_ID),
    INDEX idx_plan_validity (IMEI, Plan_ID, date_of_purchase)  -- Added index for plan validity checks
);

CREATE TABLE IF NOT EXISTS uses (
    usage_quantum INT NOT NULL,
    IMEI CHAR(15) NOT NULL,
    Tower_ID INT NOT NULL,
    time_stamp TIMESTAMP NOT NULL,
    PRIMARY KEY (IMEI, time_stamp),
    FOREIGN KEY (IMEI) REFERENCES Device(IMEI),
    FOREIGN KEY (Tower_ID) REFERENCES Towers(Tower_ID),
    INDEX idx_tower_usage (Tower_ID, time_stamp),  -- Added index for tower_load function
    CHECK (usage_quantum >= 0)
);
-- Function to find load on a given tower in a given time period
DELIMITER |
CREATE FUNCTION IF NOT EXISTS tower_load (tower_id INT, period_start TIMESTAMP, period_end TIMESTAMP)
RETURNS DECIMAL(10,2)                    -- Changed to DECIMAL for more precise load calculation
DETERMINISTIC
BEGIN
    DECLARE usage_total INT;
    DECLARE capacity INT;
    
    SELECT COALESCE(SUM(usage_quantum), 0)  -- Handle NULL case
    INTO usage_total
    FROM uses
    WHERE
        uses.Tower_ID = tower_id AND
        uses.time_stamp > period_start AND 
        uses.time_stamp < period_end;
        
    SELECT Tower_Capacity
    INTO capacity
    FROM Towers
    WHERE Towers.Tower_ID = tower_id;
    
    IF capacity IS NULL OR capacity = 0 THEN
        RETURN 0;                           -- Prevent division by zero
    END IF;
    
    RETURN CAST(usage_total AS DECIMAL(10,2)) / CAST(capacity AS DECIMAL(10,2));
END |
DELIMITER ;

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
        User_plan.Plan_ID = plan_spec.Plan_ID and
        DATE_ADD(User_plan.date_of_purchase, INTERVAL plan_spec.validity_days DAY) > NEW.time_stamp;

    IF @valid_plans = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User does not have any valid pack';
    END IF;
END |
DELIMITER ;

-- trigger for preventing tower overload

-- Updated trigger with NULL handling
DELIMITER //

CREATE TRIGGER prevent_tower_overload
BEFORE INSERT ON uses
FOR EACH ROW
BEGIN
    DECLARE current_load DECIMAL(10,2);
    DECLARE tower_capacity INT;

    -- Modified query to handle NULL cases with COALESCE
    SELECT
        COALESCE(
            CAST(COALESCE(SUM(usage_quantum), 0) AS DECIMAL(10,2)) /
            NULLIF(CAST(Towers.Tower_Capacity AS DECIMAL(10,2)), 0),
            0
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
    IF (current_load + CAST(NEW.usage_quantum AS DECIMAL(10,2)) / CAST(tower_capacity AS DECIMAL(10,2)) > 1) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Tower capacity exceeded, connection denied.';
    END IF;
END //

DELIMITER ;
CREATE USER IF NOT EXISTS 'analyst'; -- Analysts who work with the database

-- Restricted information
CREATE VIEW user_filtered
AS
    SELECT User_phone_number, IMEI, city, state FROM User;
GRANT SELECT ON user_filtered TO 'analyst';


-- Queries

-- 1. Plan popularity with names
CREATE VIEW plan_popularity_ AS
SELECT ps.Plan_name, COUNT(*) as subscribers
FROM User_plan up
JOIN plan_spec ps ON ps.Plan_ID = up.Plan_ID
GROUP BY ps.Plan_ID, ps.Plan_name
ORDER BY subscribers DESC;

-- 2. Tower load for a specific tower
-- 3. User distribution across cities
CREATE VIEW user_distribution_ AS
SELECT city, COUNT(*) as user_count
FROM User
GROUP BY city
ORDER BY user_count DESC;

-- 4. Device type distribution
CREATE VIEW device_distribution_ AS
SELECT device_type, COUNT(*) as device_count
FROM Device
GROUP BY device_type;

-- 5. Average tower capacity by business user
CREATE VIEW avg_tower_capac_bu_ AS
SELECT bu.Business_name, AVG(t.Tower_Capacity) as avg_capacity
FROM Towers t
JOIN Business_user bu ON bu.Business_user_ID = t.Business_user_ID
GROUP BY bu.Business_user_ID, bu.Business_name;


-- 6 All currently running plans
CREATE VIEW running_plans_ AS
SELECT up.*
FROM User_plan up
JOIN plan_spec ps ON up.Plan_ID = ps.Plan_ID
WHERE DATE_ADD(up.date_of_purchase, INTERVAL ps.validity_days DAY) > NOW();


-- 7 Users with multiple active plans
CREATE VIEW multi_plan_ AS
SELECT u.User_name, COUNT(DISTINCT up.Plan_ID) as active_plans
FROM User u
JOIN User_plan up ON u.IMEI = up.IMEI
JOIN running_plans_ rp ON up.IMEI = rp.IMEI
GROUP BY u.User_name
HAVING active_plans > 1;

-- 8. tower load
-- 9. all users
-- 10. update user mails
-- 11. User usage
-- 12. Idle users
