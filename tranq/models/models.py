import sqlite3
from sqlite3 import Error

from typing import List, Dict, Optional, Any, Union


class User:
    def __init__(
        self,
        conn: sqlite3.Connection
    ) -> None:
        """
        Initialize a new User object

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database
        """
        self.conn = conn
        self.ensure_table()

    def ensure_table(self) -> None:
        """
        Ensure that the `users` table exists in the database

        This method checks if the `users` table exists, and if it does not,
        creates the table. Ensures that the table is in place
        before any operations are performed on it
        """
        try:
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `username` TEXT NOT NULL,
                `email` TEXT NOT NULL,
                `password_hash` TEXT NOT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `first_name` TEXT,
                `last_name` TEXT
            );"""
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.conn.commit()
        except Error as e:
            print(e)

    def add_user(
        self,
        user_info: Dict[str, str]
    ) -> Optional[int]:
        """
        Adds a new user to the database

        Args:
            user_info (Dict[str, Any]): A dictionary containing the user's information.
            Expected keys are 'first_name', 'last_name', 'email', 'username', 'password_hash'

        Returns:
            Optional[int]: The ID of the newly added user, or None if the operation failed
        """

        # user_info oshould be a dict with the same key names as the cols here)
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO `users` (
                `first_name`,
                `last_name`,
                `email`,
                `username`,
                `password_hash`
            )
            VALUES(
                :first_name,
                :last_name,
                :email,
                :username,
                :password_hash
            );""",
            user_info
        )
        self.conn.commit()
        return cur.lastrowid

    def update_user(
        self,
        user_info: Dict[str, str]
    ) -> bool:
        """
        Update a user's information in the database

        Args:
            user_info (Dict[str, Any]): A dictionary containing the updated user's information.
            Expected keys are the column names to be updated and the 'id' of the user.

        Returns:
            bool: True if the user's information was updated, False otherwise.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE users
            SET first_name = :first_name,
                last_name = :last_name,
                email = :email,
                username = :username
            WHERE id = :id
            ;""",
            user_info   # dict has keys matching the colnames with corresponding values
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete_user(
        self,
        user_id: int
    ) -> bool:
        """
        Delete a user from the database

        Args:
            user_id (int): The 'id' of the user to be deleted.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            DELETE FROM `users`
            WHERE `id`=:user_id
            ;""",
            {'user_id': user_id}
        )
        self.conn.commit()
        return cur.rowcount > 0

    def get_user_by_id(
        self,
        user_id: int
    ) -> Optional[sqlite3.Row]:
        """
        Retrieve a user's information from the database by 'id'

        Args:
            user_id (int): The 'id' of the user to be retrieved

        Returns:
            Optional[sqlite3.Row]: The user's information as a sqlite3.Row object,
            or None if no user was found with the provided 'id'
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `users`
            WHERE `id`=:user_id
            ;""",
            {'user_id': user_id}
        )
        user = cur.fetchone()

        return user

    def get_user_by_username(
        self,
        username: str
    ) -> Optional[sqlite3.Row]:
        """
        Retrieve a user's information from the database by username

        Args:
            username (str): The username of the user to be retrieved

        Returns:
            Optional[sqlite3.Row]: The user's information as a sqlite3.Row object,
            or None if no user was found with the provided username
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `users`
            WHERE `username`=:username
            ;""",
            {'username': username}
        )
        user = cur.fetchone()

        return user


class Token:
    def __init__(
        self,
        conn: sqlite3.Connection
    ) -> None:
        """
        Initialize a new Token object.

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database
        """
        self.conn = conn
        self.ensure_table()

    def ensure_table(self) -> None:
        """
        Ensure that the `tokens` table exists in the database

        This method checks if the `tokens` table exists, and if it does not,
        creates the table.
        """
        try:
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS `tokens` (
                `token_hash` TEXT NOT NULL,
                `user_id` INTEGER,
                FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
            );"""
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.conn.commit()

        except Error as e:
            print(e)

    def add_token(
        self,
        token_info: Dict[str, Union[str, int]]
    ) -> Optional[int]:
        """
        Adds a new token to the database

        Args:
            token_info (Dict[str, Union[str, int]]): A dictionary containing the token's information.
            Expected keys are 'token_hash' and 'user_id'

        Returns:
            Optional[int]: The ID of the newly added token, or None if the operation failed.
        """

        # token_inf oshould be a dict with the same key names as the cols here)
        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO `tokens` (
                `token_hash`,
                `user_id`
            )
            VALUES(:token_hash, :user_id)
            ;""",
            token_info
        )
        self.conn.commit()
        return cur.lastrowid

    def delete_token(
        self,
        token_hash: str
    ) -> bool:
        """
        Delete a token from the database.

        Args:
            token_hash (str): The token to be deleted.

        Returns:
            bool: True if the token was deleted, False otherwise.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            DELETE FROM `tokens`
            WHERE `token_hash`=:token_hash
            ;""",
            {'token_hash': token_hash}
        )
        self.conn.commit()
        return cur.rowcount > 0

    def user_join_tokens(
        self,
        token_hash: str
    ) -> Optional[sqlite3.Row]:
        """
        Retrieve a user's information and associated token from the database by token hash.

        Args:
            token_hash (str): The hash of the token associated with the user to be retrieved.

        Returns:
            Optional[sqlite3.Row]: The user's information and associated token as a sqlite3.Row object,
            or None if no user was found with the provided token hash.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `users`
            JOIN `tokens`
            ON `users`.`id` = `tokens`.`user_id`
            WHERE `tokens`.`token_hash`=:token_hash
            ;""",
            {'token_hash': token_hash}
        )
        user_with_token = cur.fetchone()

        return user_with_token


class Trip:
    def __init__(
        self,
        conn: sqlite3.Connection
    ) -> None:
        """
        Initialize a new Trip object.

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database
        """
        self.conn = conn
        self.ensure_table()

    def ensure_table(self) -> None:
        """
        Ensure that the `trips` table exists in the database

        This method checks if the `trips` table exists, and if it does not,
        creates the table.
        """
        try:
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS `trips` (
                    `trip_id` INTEGER PRIMARY KEY AUTOINCREMENT,
                    `user_id` INTEGER,
                    `trip_name` TEXT,
                    `start_date` TEXT NOT NULL,  -- store as "YYYY-MM-DD",
                    `end_date` TEXT NOT NULL,  -- store as "YYYY-MM-DD",
                    `destination` TEXT NOT NULL,
                    `origin` TEXT NOT NULL,
                    `trip_status` TEXT,
                    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `description` TEXT
                    CHECK(LENGTH(description) <= 250),
                FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
            );
            """
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.conn.commit()
        except Error as e:
            print(e)

    def add_trip(
        self,
        trip_info: Dict[str, Any]
    ) -> Optional[int]:
        """
        Adds a new trip to the database

        Args:
            trip_info (Dict[str, Any]): A dictionary containing the token's information.
            Expected keys are 'token_hash' and 'user_id'

        Returns:
            Optional[int]: The ID of the newly added trip, or None if the operation failed.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO `trips` (
                `trip_name`,
                `start_date`,
                `end_date`,
                `destination`,
                `origin`,
                `trip_status`,
                `user_id`,
                `description`
                )
                VALUES(
                :trip_name,
                :start_date,
                :end_date,
                :destination,
                :origin,
                :trip_status,
                :user_id,
                :description
                )
            ;""",
            trip_info
        )
        self.conn.commit()
        return cur.lastrowid

# to be added:
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_trip(
        self,
        trip_info: Dict[str, Any]
    ) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE `trips`
            SET
                `trip_name`=:trip_name,
                `start_date`=:start_date,
                `end_date`=:end_date,
                `destination`=:destination,
                `origin`=:origin,
                `trip_status`=:trip_status,
                `user_id`=:user_id,
                `description`=:description
            WHERE trip_id=:trip_id
            ;""",
            trip_info
        )
        self.conn.commit()

    def delete_trip(
        self,
        trip_id: int
    ) -> bool:
        """
        Delete a trip from the database

        Args:
            trip_id (int): The 'id' of the trip to be deleted.

        Returns:
            bool: True if the trip was deleted, False otherwise.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            DELETE FROM `trips`
            WHERE `trip_id`=:trip_id
            ;""",
            {'trip_id': trip_id}
        )
        self.conn.commit()
        return cur.rowcount > 0
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_user_trips(
        self,
        user_id: int
    ) -> Optional[List[sqlite3.Row]]:
        """
        Retrieve a user's trip information from the database by 'user_id'

        Args:
            user_id (int): The 'user_id' of the trips to be retrieved

        Returns:
            Optional[List[sqlite3.Row]]: The user's trip information as a list of sqlite3.Row objects,
            or None if no trips were found for the provided 'user_id'
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `trips`
            WHERE `user_id`=:user_id
            ;""",
            {'user_id': user_id}
        )
        trips_list = cur.fetchall()

        return trips_list

    def select_trip_by_trip_id(
        self,
        trip_id: int
    ) -> Optional[sqlite3.Row]:
        """
        Retrieve a trip's information from the database by 'trip_id'

        Args:
            trip_id (int): The 'trip_id' of the trip to be retrieved

        Returns:
            Optional[sqlite3.Row]: The trip's information as a sqlite3.Row object,
            or None if no trip was found with the provided 'trip_id'
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `trips`
            WHERE `trip_id`=:trip_id
            ;""",
            {'trip_id': trip_id}
        )
        trip = cur.fetchone()

        return trip


class Flight:
    def __init__(
        self,
        conn: sqlite3.Connection
    ) -> None:
        """
        Initialize a new Flight object.

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database
        """
        self.conn = conn
        self.ensure_table()

    def ensure_table(self) -> None:
        """
        Ensure that the `flights` table exists in the database

        This method checks if the `flights` table exists, and if it does not,
        creates the table.
        """
        try:
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS `flights` (
                `trip_id` INTEGER,
                `confirmation` TEXT,
                `dep_date` TEXT NOT NULL,
                `airline` TEXT,
                `flight_num_iata` TEXT,
                `seat` TEXT,
                `dep_city` TEXT,
                `dep_airport` TEXT,
                `dep_airport_iata` TEXT,
                `dep_scheduled_time_loc` TEXT,
                `dep_terminal` TEXT,
                `dep_gate` TEXT,
                `arr_city` TEXT,
                `arr_airport` TEXT,
                `arr_airport_iata` TEXT,
                `arr_scheduled_time_loc` TEXT,
                `arr_pred_time_loc` TEXT,
                `arr_terminal` TEXT,
                `arr_gate` TEXT,
                `aircraft_model` TEXT,
                `aircraft_fare_class` TEXT,
                `aircraft_meal` TEXT,
                `aircraft_entertainment` TEXT,
                `aircraft_stops` TEXT,
                `aircraft_distance` TEXT,
                `aircraft_on_time` TEXT,
                `aircraft_img_url` TEXT,
                FOREIGN KEY(`trip_id`) REFERENCES `trips`(`id`),
                UNIQUE (`dep_scheduled_time_loc`, `flight_num_iata`)
            );"""
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.conn.commit()

        except Error as e:
            print(e)

    def add_flight(
        self,
        flight_info: Dict[str, Any]
    ) -> Optional[int]:
        """
        Adds new flight info to the database

        Args:
            flight_info (Dict[str, Any]): A dictionary containing the flight's relevant information.

        Returns:
            Optional[int]: The ID of the newly added trip, or None if the operation failed.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO `flights` (
                `trip_id`,
                `confirmation`,
                `dep_date`,
                `airline`,
                `flight_num_iata`,
                `seat`,
                `dep_city`,
                `dep_airport`,
                `dep_airport_iata`,
                `dep_scheduled_time_loc`,
                `dep_terminal`,
                `dep_gate`,
                `arr_city`,
                `arr_airport`,
                `arr_airport_iata`,
                `arr_scheduled_time_loc`,
                `arr_pred_time_loc`,
                `arr_terminal`,
                `arr_gate`,
                `aircraft_model`,
                `aircraft_fare_class`,
                `aircraft_meal`,
                `aircraft_entertainment`,
                `aircraft_stops`,
                `aircraft_distance`,
                `aircraft_on_time`,
                `aircraft_img_url`
            ) VALUES (
                :trip_id,
                :confirmation,
                :dep_date,
                :airline,
                :flight_num_iata,
                :seat,
                :dep_city,
                :dep_airport,
                :dep_airport_iata,
                :dep_scheduled_time_loc,
                :dep_terminal,
                :dep_gate,
                :arr_city,
                :arr_airport,
                :arr_airport_iata,
                :arr_scheduled_time_loc,
                :arr_pred_time_loc,
                :arr_terminal,
                :arr_gate,
                :aircraft_model,
                :aircraft_fare_class,
                :aircraft_meal,
                :aircraft_entertainment,
                :aircraft_stops,
                :aircraft_distance,
                :aircraft_on_time,
                :aircraft_img_url
            )
            ;""",
            flight_info
        )
        self.conn.commit()
        return cur.lastrowid

    def select_flight_by_trip_id(
            self,
            trip_id: int
    ) -> Optional[List[sqlite3.Row]]:
        """
        Retrieve a flight's information from the database by 'trip_id'

        Args:
            trip_id (int): The 'trip_id' of the trip to be retrieved

        Returns:
            Optional[sqlite3.Row]: The flight's information as a sqlite3.Row object,
            or None if no flight was found with the provided 'trip_id'
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `flights`
            WHERE `trip_id`=:trip_id
            ;""",
            {'trip_id': trip_id}
        )
        flights = cur.fetchall()
        return flights

    def select_flights_by_flight_number(
                self,
                flight_number: str
     ) -> Optional[sqlite3.Row]:
        """
        Retrieve a flight's information from the database by 'flight_number'

        Args:
            flight_number (str): The 'flight_number' of the trip to be retrieved

        Returns:
            Optional[sqlite3.Row]: The flight's information as a sqlite3.Row object,
            or None if no flight was found with the provided 'flight_number'
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `flights`
            WHERE `flight_num_iata`=:flight_number
            ;""",
            {'flight_number': flight_number}
        )
        flight = cur.fetchone()
        return flight


class Lodging:
    def __init__(
        self,
        conn: sqlite3.Connection
    ) -> None:
        """
        Initialize a new Lodging object.

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database
        """
        self.conn = conn
        self.ensure_table()

    def ensure_table(self) -> None:
        """
        Ensure that the `lodging` table exists in the database

        This method checks if the `lodging` table exists, and if it does not,
        creates the table.
        """
        try:
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS `lodging` (
                `lodging_id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `trip_id` INTEGER,
                `lodging_name` TEXT,
                `lodging_type` TEXT,
                `address` TEXT,
                `contact_number` TEXT,
                `email` TEXT,
                `website` TEXT,
                `price_per_night` TEXT,
                `number_of_rooms` TEXT,
                `rating` TEXT,
                `amenities` TEXT,
                `check_in_time` TEXT,
                `check_out_time` TEXT,
                `availability` TEXT,
                `images` TEXT,
                FOREIGN KEY(`trip_id`) REFERENCES `trips`(`id`)
            );"""
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.conn.commit()

        except Error as e:
            print(e)

    def add_lodging(
        self,
        lodging_info: Dict[str, Any]
    ) -> Optional[int]:
        """
        Adds new lodging info to the database

        Args:
            lodging_info (Dict[str, Any]): A dictionary containing the lodging's relevant information.

        Returns:
            Optional[int]: The ID of the newly added trip, or None if the operation failed.
        """

        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO `lodging` (
                `trip_id`,
                `lodging_name`,
                `lodging_type`,
                `address`,
                `contact_number`,
                `email`,
                `website`,
                `price_per_night`,
                `number_of_rooms`,
                `rating`,
                `amenities`,
                `check_in_time`,
                `check_out_time`,
                `availability`,
                `images`
            ) VALUES (
                :trip_id,
                :lodging_name,
                :lodging_type,
                :lodging_address,
                :contact_number,
                :email,
                :lodging_website,
                :price_per_night,
                :number_of_rooms,
                :rating,
                :amenities,
                :check_in_time,
                :check_out_time,
                :availability,
                :images
            )
            ;""",
            lodging_info
        )
        self.conn.commit()
        return cur.lastrowid

    def select_lodging_by_trip_id(
            self,
            trip_id: int
    ) -> Optional[List[sqlite3.Row]]:
        """
        Retrieve a lodging information from the database by 'trip_id'

        Args:
            trip_id (int): The 'trip_id' of the trip to be retrieved

        Returns:
            Optional[sqlite3.Row]: The flight's information as a sqlite3.Row object,
            or None if no lodging was found with the provided 'trip_id'
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM `lodging`
            WHERE `trip_id`=:trip_id
            ;""",
            {'trip_id': trip_id}
        )
        lodgings = cur.fetchall()
        return lodgings


# add update flight, delete flight, update lodging, delete lodging,
# after delete user -> deleter their trips,
# after deleting the trips -> delete related flights, lodging and activities
