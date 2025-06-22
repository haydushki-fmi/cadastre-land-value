import requests


def get_geoapify_isoline(latitude, longitude, travel_type, travel_mode, travel_range, api_key):
    """
    Requests an isoline from the Geoapify Isoline API.

    Args:
        latitude (float): The latitude of the starting point.
        longitude (float): The longitude of the starting point.
        travel_type (str): The type of isoline (e.g., 'time', 'distance').
        travel_mode (str): The mode of travel (e.g., 'walk', 'drive', 'bike').
        travel_range (int): The range for the isoline in seconds (for 'time') or meters (for 'distance').
        api_key (str): Geoapify API key.

    Returns:
        dict: A dictionary containing the JSON response from the Geoapify API,
              or None if an error occurs.
    """
    base_url = "https://api.geoapify.com/v1/isoline"
    params = {
        "lat": latitude,
        "lon": longitude,
        "type": travel_type,
        "mode": travel_mode,
        "range": travel_range,
        "apiKey": api_key
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()
