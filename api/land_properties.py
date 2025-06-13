import json

from flask import Blueprint, jsonify, request, current_app
from shapely.geometry.geo import shape
from shapely.geometry.point import Point
from shapely.prepared import prep

from db import get_db
from geoapify import get_geoapify_isoline
from overpass import get_amenities_within_radius

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


@land_properties.route('/get-value', methods=['GET'])
def get_value():
    lat = request.args.get('lat', 42.6977, type=float)
    lon = request.args.get('lon', 23.3242, type=float)
    travel_type = request.args.get('travel_type', 'time', type=str)
    travel_mode = request.args.get('travel_mode', 'walk', type=str)
    travel_range = request.args.get('travel_range', '600', type=int)
    amenity_type = request.args.get('amenity_type', 'hospital', type=str)

    geoapify_api_key = current_app.config['GEOAPIFY_API_KEY']
    try:
        isoline_polygon = get_geoapify_isoline(lat, lon, travel_type, travel_mode, travel_range, geoapify_api_key)
        prepared_isoline = prep(shape(isoline_polygon['features'][0]['geometry']))

        overpass_amenities = get_amenities_within_radius(lat, lon, 1000, amenity_type)

        amenities_within_isoline = []
        for amenity in overpass_amenities:
            if amenity['lat'] is not None and amenity['lon'] is not None:
                # Shapely Point expects (longitude, latitude)
                point = Point(amenity['lon'], amenity['lat'])
                if prepared_isoline.contains(point):
                    amenities_within_isoline.append(amenity)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    geojson_features = []
    for amenity in amenities_within_isoline:
        if 'lat' not in amenity or 'lon' not in amenity or 'id' not in amenity:
            continue

        geometry = {
            'type': 'Point',
            'coordinates': [amenity['lon'], amenity['lat']]
        }

        properties = {
            'id': amenity['id']
        }

        if 'tags' in amenity and isinstance(amenity['tags'], dict):
            properties['name'] = amenity['tags'].get('name', 'Unnamed Amenity')
        else:
            properties['name'] = 'Unknown'

        feature = {
            'type': 'Feature',
            'geometry': geometry,
            'properties': properties
        }
        geojson_features.append(feature)

    geojson_features.append(isoline_polygon['features'][0])
    geojson_data = {
        'type': 'FeatureCollection',
        'features': geojson_features
    }

    return jsonify(geojson_data)
