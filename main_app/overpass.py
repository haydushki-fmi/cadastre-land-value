import overpy


def get_amenities_within_radius(latitude, longitude, radius_meters, amenity_type=None):
    """
    Requests amenities within a specified radius of a given point from the Overpass API.

    Args:
        latitude (float): The latitude of the center point.
        longitude (float): The longitude of the center point.
        radius_meters (int): The radius in meters to search for amenities.
        amenity_type (str, optional): The specific amenity type to search for (e.g., 'restaurant', 'park', 'hospital').
                                      If None, all amenities will be returned.

    Returns:
        list: A list of dictionaries, where each dictionary represents an amenity
              (node, way, or relation) with its ID, type, latitude, longitude, and tags.
              Returns an empty list if no amenities are found or an error occurs.
    """
    api = overpy.Overpass()

    # Construct the Overpass QL query
    # nwr means nodes, ways, and relations
    # around:radius,lat,lon filters by radius around a coordinate
    # out geom includes geometry information (for ways and relations)
    query_parts = [
        f"[out:json][timeout:90];",
        f"("
    ]

    if amenity_type:
        query_parts.append(f"  nwr[\"amenity\"=\"{amenity_type}\"](around:{radius_meters},{latitude},{longitude});")
    else:
        query_parts.append(f"  nwr[\"amenity\"](around:{radius_meters},{latitude},{longitude});")

    query_parts.append(f");")
    query_parts.append(f"out center;")

    overpass_query = "\n".join(query_parts)

    result = api.query(overpass_query)

    amenities = []
    # Process nodes
    for node in result.nodes:
        amenities.append({
            "id": node.id,
            "type": "node",
            "lat": float(node.lat),
            "lon": float(node.lon),
            "tags": node.tags
        })

    # Process ways
    for way in result.ways:
        # Overpass 'out center' provides a centroid for ways and relations
        # For full geometry, use 'out geom' and parse the 'geometry' attribute.
        amenities.append({
            "id": way.id,
            "type": "way",
            "lat": float(way.center_lat) if way.center_lat else None,
            "lon": float(way.center_lon) if way.center_lon else None,
            "tags": way.tags
        })

    # Process relations
    for relation in result.relations:
        amenities.append({
            "id": relation.id,
            "type": "relation",
            "lat": float(relation.center_lat) if relation.center_lat else None,
            "lon": float(relation.center_lon) if relation.center_lon else None,
            "tags": relation.tags
        })

    return amenities
