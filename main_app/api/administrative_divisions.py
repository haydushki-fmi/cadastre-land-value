from flask import Blueprint, jsonify

from main_app.db import get_db

administrative_divisions = Blueprint('administrative_divisions', __name__, url_prefix='/api/administrative-divisions')


@administrative_divisions.route('/', methods=['GET'])
def get_administrative_divisions():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                sql_query = "SELECT id, obns_cyr FROM administrative_divisions;"
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                return jsonify(rows)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
