from flask import g, render_template, request, redirect, make_response
from flask import Blueprint

from tranq.models.models import User, Token, Trip
from tranq.utils.utils import PasswordManager

users = Blueprint('users', __name__)

# dance monkey, monster rihanna


@users.before_request
def before_request():
    g.user_model = User(g.db)
    g.token_model = Token(g.db)
    g.trip_model = Trip(g.db)


@users.get('/')
def login_page():

    if request.cookies.get('token_hash'):
        return redirect('/feed')

    err = request.args.get('err')
    if err:
        error = "Invalid username or password."
    else:
        error = ""

    return render_template("login.html", error=error)


@users.post('/')
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    user = g.user_model.get_user_by_username(username)
    new_token_hash = PasswordManager.generate_token_hash(username)

    new_token_info = {
        'token_hash': new_token_hash,
        'user_id': user['id']
    }
    g.token_model.add_token(new_token_info)

    if not user:
        # return redirect('/login/err')
        return redirect('/login?err=invalid')

    if not PasswordManager.check_password_hash(
        user['password_hash'],
        password
    ):
        # return redirect('/login/err')
        return redirect('/login?err=invalid')

    response = make_response(redirect('/feed'))
    response.set_cookie('token_hash', new_token_hash)
    return response


@users.get('/signup')
def signup_pg():
    if request.cookies.get('token_hash'):
        return redirect('/feed')
    else:
        return render_template("signup.html")


@users.post('/signup')
def signup_new_user():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    email = request.form.get('email')
    password_hash = PasswordManager.generate_password_hash(password)
    token_hash = PasswordManager.generate_token_hash(username)

    new_user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'password_hash': password_hash,

    }
    g.user_model.add_user(new_user)

    token_info = {
        'token_hash': token_hash,
        'user_id': g.user_model.get_user_by_username(username)['id']
    }

    g.token_model.add_token(token_info)
    return redirect('/')


@users.post('/logout')
def logout_user():
    token_hash = request.cookies.get('token_hash')
    g.token_model.delete_token(token_hash)

    response = make_response(redirect('/'))
    response.delete_cookie('token_hash')

    return response
