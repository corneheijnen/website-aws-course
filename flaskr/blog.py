from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from flaskr.auth import login_required
from flaskr.db import get_db
from sqlalchemy.sql import text

blueprint = Blueprint('blog', __name__, url_prefix='/')


@blueprint.route('/')
def index():
    db = get_db()
    posts = db.execute(text("""SELECT p.id, title, body, created, author_id, username
                       FROM post p JOIN user u ON p.author_id = u.id
                       ORDER BY created DESC""")).fetchall()
    return render_template('blog/index.html', posts=posts)


@blueprint.route('create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(text(
                """INSERT INTO post (title, body, author_id)
                VALUES (:title, :body, :id)"""), parameters={"title": title, "body": body, "id": g.user[0]})
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(text(
        """SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = :id """), {'id': id}).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post[-2] != g.user[0]:
        print(post[1])
        print(post)
        print(g.user[0])
        abort(403)

    return post


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(text("""UPDATE post SET title = :title, body = :body
                       WHERE id = :id"""), {'title': title, 'body': body, 'id': id})
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(text('DELETE FROM post WHERE id = :id'), {'id': id})
    db.commit()
    return redirect(url_for('blog.index'))
