from flask import Flask, render_template

from .config import config_by_name


def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    from . import db
    db.init_app(app)

    @app.route('/database')
    def database():
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

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

    from api.land_properties import land_properties
    app.register_blueprint(land_properties)
    return app
