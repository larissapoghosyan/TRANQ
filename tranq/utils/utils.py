from random import randint
from datetime import datetime
from tranq.app.extensions import bcrypt
from typing import Optional


class PasswordManager:
    @staticmethod
    def generate_password_hash(
        password: str
    ) -> str:
        """
        Generates a bcrypt hashed version of the input password.

        Args:
            password (str): Password to hash.

        Returns:
            str: Hashed password.
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def generate_token_hash(
        username: str
    ) -> str:
        """
        Generates a unique token hash for a given username.

        Args:
            username (str): Username to generate token for.

        Returns:
            str: Unique token hash.
        """
        random_ints = [randint(1, 100) for _ in range(5)]
        random_ints_str = ' '.join(
            map(str, random_ints)
        )
        return bcrypt.generate_password_hash(
            username + random_ints_str
        ).decode('utf-8')

    @staticmethod
    def check_password_hash(hashed_password: str, password: str) -> bool:
        return bcrypt.check_password_hash(hashed_password, password)


class DateFormatter:
    @staticmethod
    def format_trip_dates(
        start_date_text: str,
        end_date_text: str
    ):
        """
        Formats start and end dates, and calculates the number of days between them.

        Args:
            start_date_text (str): Start date in "YYYY-MM-DD" format.
            end_date_text (str): End date in "YYYY-MM-DD" format.

        Returns:
            str: Formatted date string.

        Raises:
            ValueError: If dates are not in the expected format.
        """
        try:
            start_date = datetime.strptime(start_date_text, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Dates must be in 'YYYY-MM-DD' format")

        start_date_str = start_date.strftime('%a %d %b')
        end_date_str = end_date.strftime('%a %d %b')
        num_days = (end_date - start_date).days + 1

        date_string = f'{start_date_str} - {end_date_str} ({num_days} days)'
        return date_string

    @staticmethod
    def format_date(
        date_text: str
    ):
        """
        Converts a date string in the format "YYYY-MM-DD" from the SQLite database
        to a datetime.date object.

        Args:
            date_text (str): The date string to convert.

        Returns:
            datetime (date obj): The converted date.
        """
        try:
            return datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            print(f"Unable to parse date: {date_text}")
            return

    @staticmethod
    def format_date_for_db(
        date: datetime
    ):
        """
        Converts a datetime.date object to a string in the format "YYYY-MM-DD" for
        insertion into the SQLite database.

        Args:
            date (datetime): The date to convert.

        Returns:
            str: The converted date string.
        """
        try:
            return date.strftime("%Y-%m-%d")
        except ValueError:
            print("Unable to parse date")
            return

    @staticmethod
    def format_date_with_gmt(
        datetime_str: str
    ):
        """
        Formats a date-time string to include "GMT+02:00".

        Args:
            datetime_str (str): Date-time string in "YYYY-MM-DD HH:MM+02:00" format.

        Returns:
            str: Formatted date-time string with GMT offset.
        """
        try:
            datetime_obj = datetime.fromisoformat(datetime_str)
            date_time_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S GMT%z')
            # Insert the colon into the offset
            date_time_str = date_time_str[:-2] + ':' + date_time_str[-2:]
            return date_time_str
        except ValueError:
            print(f"Unable to parse date-time: {datetime_str}")
            return

    @staticmethod
    def format_date_with_weekday_monthday(date_str: str):
        """
        Formats a date string to "Sat, Aug 10" format.

        Args:
            date_str (str): Date string in "YYYY-MM-DD" format.

        Returns:
            str: Formatted date string with weekday, month, and day.
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            date_str_formatted = date_obj.strftime('%a, %b %d')
            return date_str_formatted
        except ValueError:
            print(f"Unable to parse date: {date_str}")
            return


class EmailValidator:
    @staticmethod
    def validate(email: str) -> None:
        pass


class PaginationHandler:
    @staticmethod
    def handle_pagination(page, items_per_page, items):
        pass


class DataProcessor:
    @staticmethod
    def data_processing():
        pass
