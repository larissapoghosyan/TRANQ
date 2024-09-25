import requests
from typing import Dict, Any


class FlightDataRequest:
    def __init__(self):

        self.headers = {
            "x-rapidapi-key": "c72754bb8cmsh0af90b1a4f91942p16c97fjsnb83506cf593f",
            "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
        }

    def get_schedule_by_date_range(
        self,
        airport_iata: str,
        dep_date: str,
        arr_date: str,
    ) -> Dict[Any, Any]:
        url = f'https://aerodatabox.p.rapidapi.com/flights/airports/iata/{airport_iata}/{dep_date}/{arr_date}'    
        # '2024-08-15T08:00/2024-08-15T12:00'
        querystring = {
            "withLeg": "true",
            "direction": "Both",
            "withCancelled": "true",
            "withCodeshared": "true",
            "withCargo": "false",
            "withPrivate": "false",
            "withLocation": "true"
        }

        response = requests.get(url, headers=self.headers, params=querystring)

        return response.json()

    def get_flight_info_by_date(
        self,
        flight_num_iata: str,
        dep_date: str
    ) -> Dict[Any, Any]:

        url = f'https://aerodatabox.p.rapidapi.com/flights/number/{flight_num_iata}/{dep_date}'

        querystring = {
            "withAircraftImage": "true",
            "withLocation": "true"
        }

        response = requests.get(url, headers=self.headers, params=querystring)

        return response.json()
