from flask import Blueprint, jsonify, request, current_app
from shapely.geometry.geo import shape
from shapely.geometry.point import Point
from shapely.prepared import prep

from geoapify import get_geoapify_isoline
from overpass import get_amenities_within_radius

isoline_amenities = Blueprint('isoline-amenities', __name__, url_prefix='/api/isoline-amenities')


@isoline_amenities.route('/', methods=['GET'])
def get_isoline_amenities():
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
