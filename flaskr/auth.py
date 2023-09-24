import functools
from sqlite3 import IntegrityError

import sqlalchemy
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flaskr.db import get_db

# Instantiate the blueprint for use in the app
blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                with get_db() as db:
                    db.execute(text(
                        """INSERT INTO user(username, password) VALUES (:username, :password)"""),
                        {'username': username, 'password': generate_password_hash(password)},
                    )
                    db.commit()
                    db.close()
            # except db.IntegrityError:
            except sqlalchemy.exc.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        with get_db() as db:
            user = db.execute(text("""SELECT * FROM user WHERE username = :username"""), {'username': username}).fetchone()
            db.close()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[-1], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db() as db:
            g.user = db.execute(text("""SELECT * FROM user WHERE id = :user_id"""),
                                      {'user_id': user_id}).fetchone()
            db.close()

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
