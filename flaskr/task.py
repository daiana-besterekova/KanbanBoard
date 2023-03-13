from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__)

# when at / select user info from database
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, status, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('task/index.html', posts=posts, data=['To Do','In Process', 'Done'])

# create a task and/or show error message when values are missing
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, status, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, status, g.user['id'])
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html', data=['To Do','In Process', 'Done'])

# get a task and/or show error message when values are missing
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, status, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))

# update a task and/or show error message when values are missing
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, status = ?'
                ' WHERE id = ?',
                (title, body, status, id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', post=post, data=['To Do','In Process', 'Done'])

# delete a task and redirect to index page
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.index'))

@bp.route('/<int:id>/todoing', methods=('GET', 'POST'))
@login_required
# move tasks to "In Process" and save updates in the database
def todoing(id):
    get_post(id)
    db = get_db()
    db.execute('UPDATE post SET status = ?'
                ' WHERE id = ?',
                ("In Process", id)
    )
    db.commit()
    return redirect(url_for('task.index'))

# move tasks to "Done" and save updates in the database
@bp.route('/<int:id>/todonetask', methods=('GET', 'POST'))
@login_required
def todonetask(id):
    get_post(id)
    db = get_db()
    db.execute('UPDATE post SET status = ?'
                ' WHERE id = ?',
                ('Done', id)
    )
    db.commit()
    return redirect(url_for('task.index'))

# move tasks to "To Do" and save updates in the database
@bp.route('/<int:id>/todotask', methods=('GET', 'POST'))
@login_required
def todotask(id):
    get_post(id)
    db = get_db()
    db.execute('UPDATE post SET status = ?'
                ' WHERE id = ?',
                ('To Do', id)
    )
    db.commit()
    return redirect(url_for('task.index'))