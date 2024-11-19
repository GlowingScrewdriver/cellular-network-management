import mysql.connector
from datetime import datetime, timedelta
from typing import Dict, Generator, Any, Optional


class CellularNetworkOperator:

    def __init__(self, host: str = '127.0.0.1', user: str = 'root',
                 password: str = '', database: str = 'cellular_network'):
        """Initialize database connection with error handling."""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            raise Exception(f"Failed to connect to database: {err}")

    def __del__(self):
        """Ensure proper cleanup of database connections."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def register_device(self, device_type: str = None, imei: str = None) -> None:
        """
        Register a new device in the network.

        Args:
            device_type: Either 'smartphone', 'featurephone', or None (defaults to None)
            imei: 15-character IMEI number (required)
        """
        try:
            # Validate IMEI
            if not isinstance(imei, str) or len(imei) != 15:
                raise ValueError("IMEI must be a 15-character string")

            # Validate device_type if provided (allow None)
            if device_type is not None and device_type not in ('smartphone', 'featurephone'):
                raise ValueError("device_type must be 'smartphone', 'featurephone', or None")

            # Insert into the database
            insert_query = "INSERT INTO Device (device_type, IMEI) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (device_type, imei))

            # Call the stored procedure
            self.cursor.execute("CALL UpdateNullDeviceType()")

            self.connection.commit()

        except mysql.connector.Error as err:
            self.connection.rollback()
            raise Exception(f"Failed to register device: {err}")
    def register_user(self, name: str, phone: str, apt_name: str,
                      street_name: str, city: str, pincode: str,
                      state: str, email: str, identity_proof: int,
                      imei: str) -> None:
        """
        Register a new user with their device.

        Args:
            name: User's full name
            phone: 10-digit phone number
            apt_name: Apartment/building name
            street_name: Street name
            city: City name
            pincode: 6-digit pincode
            state: State name
            email: Email address
            identity_proof: Identity proof number
            imei: Device IMEI number
        """
        try:
            query = """
                INSERT INTO User (
                    User_name, User_phone_number, apt_name, street_name,
                    city, pincode, state, User_Email, identity_proof, IMEI
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, phone, apt_name, street_name, city, pincode,
                      state, email, identity_proof, imei)
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            raise Exception(f"Failed to register user: {err}")

    def purchase_plan(self, plan_id: int, imei: str,
                      phone_number: str) -> None:
        """
        Register a new plan purchase for a user.

        Args:
            plan_id: ID of the plan being purchased
            imei: Device IMEI number
            phone_number: User's phone number
        """
        try:
            query = """
                INSERT INTO User_plan (Plan_ID, IMEI, User_phone_number, date_of_purchase)
                VALUES (%s, %s, %s, NOW())
            """
            self.cursor.execute(query, (plan_id, imei, phone_number))
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            raise Exception(f"Failed to purchase plan: {err}")

    def get_plans(self) -> Generator[Dict[str, Any], None, None]:
        """Retrieve all available plans."""
        return self.get_table("plan_spec")



    def get_tower_load(self, tower_id: int,
                       period_start: Optional[datetime] = None,
                       period_end: Optional[datetime] = None) -> float:
        """
        Get the load on a specific tower for a given time period.

        Args:
            tower_id: ID of the tower
            period_start: Start of the period (defaults to 1 month ago)
            period_end: End of the period (defaults to now)
        """
        if period_start is None:
            period_start = datetime.now() - timedelta(days=30)
        if period_end is None:
            period_end = datetime.now()

        query = "SELECT tower_load(%s, %s, %s) as `load`"
        self.cursor.execute(query, (tower_id, period_start, period_end))
        result = self.cursor.fetchone()
        return result['load'] if result else 0.0

    def get_table(self, table_name: str) -> Generator[Dict[str, Any], None, None]:
        """
        Generic method to fetch all rows from a table.

        Args:
            table_name: Name of the table to query
        """
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            for row in self.cursor:
                yield row
        except mysql.connector.Error as err:
            raise Exception(f"Failed to fetch data from {table_name}: {err}")

    def list_users(self):
        """
        List all users in the database
        """
        query = "SELECT User_name, User_phone_number FROM User"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall() or {}
        except mysql.connector.Error as err:
            raise Exception(f"Failed to fetch users: {err}")

    def get_user_details(self, phone_number: str) -> Dict[str, Any]:
        """
        Get details of a specific user.

        Args:
            phone_number: User's phone number
        """
        try:
            query = "SELECT * FROM User WHERE User_phone_number = %s"
            self.cursor.execute(query, (phone_number,))
            return self.cursor.fetchone() or {}
        except mysql.connector.Error as err:
            raise Exception(f"Failed to fetch user details: {err}")

    # def update_user_email(self, phone_number: str, new_email: str) -> Dict[str, Any]:
    #     """
    #     Change the email ID of a user
    #
    #     Args:
    #         phone_number: User's phone number
    #     """
    #     try:
    #         query = """
    #             UPDATE User
    #             SET User_email = %s
    #             WHERE User_phone_number = %s
    #         """
    #         self.cursor.execute(query, (new_email, phone_number))
    #         return self.cursor.fetchone() or {}
    #     except mysql.connector.Error as err:
    #         raise Exception(f"Failed to fetch user details: {err}")

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
        """
        try:
            self.cursor.execute (query, (phone_number,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            raise Exception(f"Failed to get usage statistics: {err}")

    def get_idle_users (self):
        """
        Get users who have no valid plan
        """
        query = """
            SELECT User_name, User_Email, t1.IMEI
            FROM (
                SELECT * FROM User_plan
                EXCEPT
                SELECT * FROM running_plans_
            ) AS t1, User
            WHERE
                User.IMEI = t1.IMEI AND
                User.User_phone_number = t1.User_phone_number
        """
        try:
            self.cursor.execute (query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            raise Exception(f"Failed to get usage statistics: {err}")

    def record_tower_usage(self, imei: str, tower_id: int,
                           usage_quantum: int) -> None:
        """
        Record usage of a tower by a device.

        Args:
            imei: Device IMEI number
            tower_id: ID of the tower used
            usage_quantum: Amount of usage
        """
        try:
            query = """
                INSERT INTO uses (usage_quantum, IMEI, Tower_ID, time_stamp)
                VALUES (%s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                usage_quantum = usage_quantum + VALUES(usage_quantum),
                time_stamp = NOW()
            """
            self.cursor.execute(query, (usage_quantum, imei, tower_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            self.connection.rollback()
            raise Exception(f"Failed to record tower usage: {err}")