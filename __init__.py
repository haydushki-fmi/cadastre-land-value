from flask import Flask

from .config import config_by_name


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    from . import db
    db.init_app(app)

    @app.route('/')
    def index():
        conn = db.get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            return f"Connected to PostgreSQL! Database version: {db_version}"
        except Exception as e:
            return f"Error connecting to database: {e}"
        finally:
            cur.close()

    return app
