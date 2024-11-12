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
    FOREIGN KEY (User_phone_number, IMEI) REFERENCES User(User_phone_number, IMEI),
    FOREIGN KEY (Plan_ID) REFERENCES plan_spec(Plan_ID)
);

CREATE TABLE IF NOT EXISTS uses (
    usage_quantum INT NOT NULL,
    IMEI CHAR(15) NOT NULL,
    Tower_ID INT NOT NULL,
    time_stamp TIMESTAMP NOT NULL,
    PRIMARY KEY (IMEI, Tower_ID),
    FOREIGN KEY (IMEI) REFERENCES Device(IMEI),
    FOREIGN KEY (Tower_ID) REFERENCES Towers(Tower_ID),
    CHECK (usage_quantum >= 0)           -- Added constraint for valid usage
);

CREATE VIEW plan_popularity AS
    SELECT Plan_ID, COUNT(*) AS user_count
    FROM User_plan
    GROUP BY Plan_ID
    ORDER BY user_count DESC;

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

-- Sample plan data
INSERT INTO plan_spec VALUES 
    (1, "Balanced", 200, 10, 80, 200),
    (2, "Entertainment", 300, 40, 60, 60),
    (3, "Talktime Add-on", 50, 0, 100, 0),
    (4, "Data Add-on", 50, 10, 0, 0);      -- Changed ID to 4 for the last plan