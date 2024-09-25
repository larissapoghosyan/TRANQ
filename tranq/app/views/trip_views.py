from flask import g, render_template, request, redirect, make_response
from flask import Blueprint

from tranq.models.models import User, Token, Trip, Flight, Lodging
from tranq.utils.utils import DateFormatter

trips = Blueprint('trips', __name__)
date_formatter = DateFormatter()


@trips.before_request
def before_request():
    g.user_model = User(g.db)
    g.token_model = Token(g.db)
    g.trip_model = Trip(g.db)
    g.flight_model = Flight(g.db)
    g.lodging_model = Lodging(g.db)


@trips.get('/feed')
def list_all_trips():
    token_hash = request.cookies.get('token_hash')
    user_join_tokens = g.token_model.user_join_tokens(token_hash)

    rows = g.trip_model.get_user_trips(user_join_tokens['user_id'])
    trip_list = [dict(row) for row in rows]
    for trip in trip_list:
        trip['date_string'] = (
            date_formatter.format_trip_dates(
                trip['start_date'],
                trip['end_date']
            )
        )

    return render_template("list_all_trips.html", trips=trip_list)


@trips.get('/new_trip')
def new_trip_pg():
    return render_template("new_trip.html")


@trips.post('/new_trip')
def add_new_trip():
    token_hash = request.cookies.get('token_hash')
    user_join_tokens = g.token_model.user_join_tokens(token_hash)

    trip_name = request.form['trip_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    destination = request.form['destination']
    origin = request.form['origin']
    trip_status = request.form['trip_status']
    trip_description = request.form['trip_description']

    new_trip = {
        "trip_name": trip_name,
        "start_date": start_date,
        "end_date": end_date,
        "destination": destination,
        "origin": origin,
        "trip_status": trip_status,
        "user_id": user_join_tokens['user_id'],
        "description": trip_description
    }

    g.trip_model.add_trip(new_trip)
    return redirect('/feed')


@trips.get('/edit_trip/<int:id>')
def updatde_trip_pg(id: int):
    token_hash = request.cookies.get('token_hash')
    user_join_tokens = g.token_model.user_join_tokens(token_hash)
    trip = g.trip_model.select_trip_by_trip_id(id)

    if trip and user_join_tokens['user_id'] == trip['user_id']:
        return render_template("update.html", trip=trip)

    return "invalid task id"


@trips.post('/edit_trip/<int:id>')
def update_trip(id: int):
    token_hash = request.cookies.get('token_hash')
    user_join_tokens = g.token_model.user_join_tokens(token_hash)

    trip_name = request.form['trip_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    destination = request.form['destination']
    origin = request.form['origin']
    trip_status = request.form['trip_status']
    trip_description = request.form['trip_description']

    new_trip = {
        "trip_id": id,
        "trip_name": trip_name,
        "start_date": start_date,
        "end_date": end_date,
        "destination": destination,
        "origin": origin,
        "trip_status": trip_status,
        "user_id": user_join_tokens['user_id'],
        "description": trip_description
    }

    try:
        g.trip_model.update_trip(new_trip)
        return redirect('/feed')

    except ValueError:
        return "error"


@trips.post('/delete_trip/<int:trip_id>')
def delete_trip(trip_id):
    g.trip_model.delete_trip(trip_id=trip_id)
    response = make_response(redirect('/feed'))
    return response


@trips.get('/list_trip_plans/<int:trip_id>')
def list_trip_plans(trip_id):
    lodging_list = g.lodging_model.select_lodging_by_trip_id(trip_id)
    lodging_list = [dict(lodging) for lodging in lodging_list]
    print(lodging_list, '********************************************************************')

    flights = g.flight_model.select_flight_by_trip_id(trip_id)
    # flight_list = [dict(flight) for flight in flights]
    # for trip in flight_list:
    #     trip['date_string'] = (
    #         date_formatter.format_trip_dates(
    #             trip['start_date'],
    #             trip['end_date']
    #         )
    #     )

    # return render_template("list_all_trips.html", trips=trip_list)
    return render_template(
        'list_trip_plans.html',
        trip_id=trip_id,
        flight_list=flights,
        lodging_list=lodging_list
    )


@trips.get('/add_trip_plans/<int:trip_id>')
def add_trip_plans(trip_id):
    return render_template('trip_plans.html', trip_id=trip_id)
