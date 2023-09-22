from sqlalchemy import create_engine

import click
from flask import current_app, g


def get_db():
    """Get the database"""
    if 'db' not in g:
        engine = create_engine(
            "mysql+pymysql://admin:j3eCawR71!@database-1.c7vm4wmhspek.eu-central-1.rds.amazonaws.com/blogpost?charset=utf8mb4")
        g.db = engine.connect()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf-8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
