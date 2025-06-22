import json

from flask import Blueprint, jsonify, request

from main_app.db import get_db

land_properties = Blueprint('land-properties', __name__, url_prefix='/api/land-properties')


@land_properties.route('/', methods=['GET'])
def get_land_properties():
    min_lon = request.args.get('min_lon', type=float)
    min_lat = request.args.get('min_lat', type=float)
    max_lon = request.args.get('max_lon', type=float)
    max_lat = request.args.get('max_lat', type=float)
    adm_div = request.args.get('adm_div', type=int)

    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                sql_query = ("SELECT ST_AsGeoJSON(ST_Transform(wkb_geometry, 4326)),"
                             " ST_AsGeoJSON(ST_Centroid(ST_Transform(wkb_geometry, 4326))),"
                             " ogc_fid, cadnum, proptype  FROM sofia_land_items")

                if all([min_lon, min_lat, max_lon, max_lat]):
                    sql_query += " WHERE ST_Intersects(wkb_geometry, ST_MakeEnvelope(%s, %s, %s, %s, 4326))"
                    cursor.execute(sql_query, (min_lon, min_lat, max_lon, max_lat))
                elif adm_div:
                    sql_query += " JOIN administrative_divisions ON ST_Intersects(wkb_geometry, geom) AND id = %s"
                    cursor.execute(sql_query, (adm_div,))
                else:
                    sql_query += " LIMIT 100"
                    cursor.execute(sql_query)

                rows = cursor.fetchall()

                geojson_data = {
                    'type': 'FeatureCollection',
                    'features': [
                        {
                            'type': 'Feature',
                            'geometry':
                                json.loads(row[0]),
                            'properties': {
                                'centroid': row[1],
                                'ogc_fid': row[2],
                                'cadnum': row[3] if row[3] else 'Unknown',
                                'proptype': row[4] if row[4] else 'Unknown'
                            },
                        } for row in rows
                    ],
                }

                return jsonify(geojson_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
