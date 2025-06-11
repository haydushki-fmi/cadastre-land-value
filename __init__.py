from flask import Flask, render_template, url_for

from .config import config_by_name


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


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

    # Just for debug purposes
    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples

        return links

    return app
