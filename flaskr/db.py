from sqlalchemy import create_engine

from flask import g


def get_db():
    """Get the database"""
    # TODO: update credentials
    engine = create_engine(
        "mysql+pymysql://admin:j3eCawR71!@database-1.c7vm4wmhspek.eu-central-1.rds.amazonaws.com/blogpost?charset=utf8mb4")
    connection = engine.connect()

    return connection

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
