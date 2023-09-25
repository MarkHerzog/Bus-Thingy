import requests

# Replace with your MapQuest API Key
MAPQUEST_API_KEY = 'C3LFx5vksRYoxuZZL9IFtiItNVAL1SLH'


def reverse_geocode(lat, lon):
    # Prepare the request data for MapQuest Reverse Geocoding API
    request_data = {
        'key': MAPQUEST_API_KEY,
        'location': f"{lat},{lon}",
    }

    # Make the API request
    response = requests.get('http://www.mapquestapi.com/geocoding/v1/reverse', params=request_data)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            location = data['results'][0]['locations'][0]['street']
            return location
        else:
            print(f"Error: Unable to fetch address for coordinates ({lat}, {lon})")
    else:
        print(f"Error: Unable to fetch address for coordinates ({lat}, {lon})")

    return None


def convert(coordinates):
    # Convert each coordinate to an address
    addresses = []
    for lat, lon in coordinates:
        address = reverse_geocode(lat, lon)
        addresses.append(address)
    return addresses