from flask import g, render_template, request, redirect, make_response, url_for
from flask import Blueprint

from tranq.models.models import User, Token, Trip, Flight, Lodging
from tranq.utils.utils import DateFormatter
from tranq.api.apisnippet import FlightDataRequest

lodging = Blueprint('lodging', __name__)
date_formatter = DateFormatter()


@lodging.before_request
def before_request():
    g.user_model = User(g.db)
    g.token_model = Token(g.db)
    g.trip_model = Trip(g.db)
    g.flight_model = Flight(g.db)
    g.lodging_model = Lodging(g.db)


@lodging.get('/add_lodging_info/<int:trip_id>')
def lodging_form(trip_id: int):
    return render_template('lodging.html', trip_id=trip_id)


@lodging.post('/add_lodging_info/<int:trip_id>')
def add_lodging(trip_id):
    lodging_name = request.form['lodging_name']
    lodging_type = request.form['lodging_type']
    lodging_address = request.form['lodging_address']
    lodging_website = request.form['lodging_website']
    price_per_night = request.form['price_per_night']
    check_in_time = request.form['check_in_time']
    check_out_time = request.form['check_out_time']

    lodging_info = {
        'trip_id': trip_id,
        'lodging_name': lodging_name,
        'lodging_type': lodging_type,
        'lodging_address': lodging_address,
        'contact_number': "",
        'email': "",
        'lodging_website': lodging_website,
        'price_per_night': price_per_night,
        'number_of_rooms': "",
        'rating': "",
        'amenities': "",
        'check_in_time': check_in_time,
        'check_out_time': check_out_time,
        'availability': "",
        'images': ""
    }
    g.lodging_model.add_lodging(lodging_info)

    return redirect(url_for('db_views.trips.list_trip_plans', trip_id=trip_id))
