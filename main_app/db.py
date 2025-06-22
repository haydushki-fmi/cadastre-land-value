import psycopg2
from flask import g, current_app


def get_db():
    if 'db' not in g:
        user = current_app.config['PG_USER']
        password = current_app.config['PG_PASSWORD']
        host = current_app.config['PG_HOST']
        port = current_app.config['PG_PORT']
        database = current_app.config['PG_DATABASE']

        conn_string = (
            f"dbname={database} user={user} password={password} "
            f"host={host} port={port}"
        )
        g.db = psycopg2.connect(conn_string)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
