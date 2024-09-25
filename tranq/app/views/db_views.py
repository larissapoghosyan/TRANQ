from flask import Blueprint
from .user_views import users
from .trip_views import trips
from .flight_views import flights
from .lodging_views import lodging
from .email_processing import emails

db_views = Blueprint('db_views', __name__)

db_views.register_blueprint(users)
db_views.register_blueprint(trips)
db_views.register_blueprint(flights)
db_views.register_blueprint(lodging)
db_views.register_blueprint(emails)
