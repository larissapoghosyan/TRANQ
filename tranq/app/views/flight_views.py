from flask import g, render_template, request, redirect, make_response, url_for
from flask import Blueprint

from tranq.models.models import User, Token, Trip, Flight
from tranq.utils.utils import DateFormatter
from tranq.api.apisnippet import FlightDataRequest

flights = Blueprint('flights', __name__)
req_flightdata = FlightDataRequest()
date_formatter = DateFormatter()


@flights.before_request
def before_request():
    g.user_model = User(g.db)
    g.token_model = Token(g.db)
    g.trip_model = Trip(g.db)
    g.flight_model = Flight(g.db)


@flights.get('/add_flight_info/<int:trip_id>')
def flight_form_pg(trip_id: int):
    return render_template('new_flight.html', trip_id=trip_id)


@flights.post('/add_flight_info/<int:trip_id>')
def add_flight(trip_id: int):
    confirmation = request.form['confirmation']
    departure_date = request.form['departure_date']
    airline = request.form['airline']
    flight_num_iata = request.form['flight_num_iata']
    seat = request.form['seat']
    fare_class = request.form['fare-class']
    meal = request.form['aircraft-meal']
    entertainment = request.form['aircraft-entertainment']

    flight_status_info = req_flightdata.get_flight_info_by_date(
                            flight_num_iata,
                            departure_date
                        )

    # posible future error --> List obj does not have attribute GET

    new_flight_status_info = []
    for info in flight_status_info:
        api_dep_date_str = info.get('departure', {}).get('scheduledTime').get('local', '').split(' ')[0]
        api_dep_date = date_formatter.format_date(api_dep_date_str)
        user_inp_dep_date = date_formatter.format_date(departure_date)

        if api_dep_date == user_inp_dep_date:
            new_flight_status_info.append(info)
            # removed .append(unfo), not to have list with length 1,
            #  idk if it can be > 1, will ask Karen Later
            # turns out it can be, need to use a unique key...

    flight_info = {
        'trip_id': trip_id,
        'confirmation': confirmation,
        'dep_date': departure_date,
        'airline': airline,
        'flight_num_iata': flight_num_iata,
        'seat': seat,
        'dep_city': '',
        'dep_airport': new_flight_status_info[0].get('departure', {}).get('airport', {}).get('name'),
        'dep_airport_iata': new_flight_status_info[0].get('departure', {}).get('airport', {}).get('iata'),
        'dep_scheduled_time_loc': new_flight_status_info[0].get('departure', {}).get('scheduledTime', {}).get('local'),
        'dep_gate': '',
        'dep_terminal': new_flight_status_info[0].get('departure', {}).get('terminal'),
        'arr_city': '',
        'arr_airport': new_flight_status_info[0].get('arrival', {}).get('airport', {}).get('iata'),
        'arr_airport_iata': new_flight_status_info[0].get('arrival', {}).get('airport', {}).get('name'),
        'arr_scheduled_time_loc': new_flight_status_info[0].get('arrival', {}).get('scheduledTime', {}).get('local'),
        'arr_pred_time_loc': new_flight_status_info[0].get('arrival', {}).get('revisedTime', {}).get('local'),
        'arr_terminal': new_flight_status_info[0].get('arrival', {}).get('terminal'),
        'arr_gate': new_flight_status_info[0].get('arrival', {}).get('gate'),
        'aircraft_fare_class': fare_class,
        'aircraft_meal': meal,
        'aircraft_entertainment': entertainment,
        'aircraft_stops': '',
        'aircraft_distance': '',
        'aircraft_on_time': '',
        'aircraft_model': new_flight_status_info[0].get('aircraft', {}).get('model'),
        'aircraft_img_url': new_flight_status_info[0].get('aircraft', {}).get('image', {}).get('url')
    }
    g.flight_model.add_flight(flight_info)

    # return render_template('new_flight.html', trip_id=trip_id)
    return redirect(url_for('db_views.trips.list_trip_plans', trip_id=trip_id))
