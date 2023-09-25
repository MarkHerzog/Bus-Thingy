import requests
import math
from scipy.cluster.hierarchy import fcluster, linkage, dendrogram
import matplotlib.pyplot as plt

# Replace with your MapQuest API Key
MAPQUEST_API_KEY = 'C3LFx5vksRYoxuZZL9IFtiItNVAL1SLH'

# Define bus stops with addresses
bus_stops = [
    "35 E Main St, Mendham, NJ 07945-1502",
    "47 E Main St, Mendham, NJ 07945-1502",
    "18 White Oak Ridge Ct, Mendham, NJ 07945-2931",
    "46 E Main St, Mendham, NJ 07945-1502"
    # Add more stops here
]

def get_lat_long(address):
    # Prepare the request data for MapQuest Geocoding API
    request_data = {
        'key': MAPQUEST_API_KEY,
        'location': address,
    }

    # Make the API request
    response = requests.get('http://www.mapquestapi.com/geocoding/v1/address', params=request_data)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            location = data['results'][0]['locations'][0]['latLng']
            return location['lat'], location['lng']
        else:
            print(f"Error: Unable to fetch coordinates for address {address}")
    else:
        print(f"Error: Unable to fetch coordinates for address {address}")

    return None, None

def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between two sets of coordinates using the Haversine formula
    R = 6371  # Radius of the Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance

def group_coordinates_by_distance(latitudes, longitudes, num_groups):
    # Combine latitudes and longitudes into a list of coordinates
    coordinates = list(zip(latitudes, longitudes))

    # Calculate the linkage matrix for hierarchical clustering
    Z = linkage(coordinates, method='ward')

    # Perform hierarchical clustering and cut the tree to get the specified number of groups
    groups = fcluster(Z, num_groups, criterion='maxclust')

    # Initialize grouped_coordinates as a list of empty lists
    grouped_coordinates = [[] for _ in range(num_groups)]

    # Assign coordinates to their respective groups
    for i, (lat, lon) in enumerate(coordinates):
        group = groups[i] - 1  # Adjust for 0-based indexing
        grouped_coordinates[group].append((lat, lon))

    return grouped_coordinates

def main():
    # Get the latitude and longitude for each address
    latitudes = []
    longitudes = []

    for address in bus_stops:
        lat, lng = get_lat_long(address)
        latitudes.append(lat)
        longitudes.append(lng)

        print(f"Address: {address}")
        print(f"Latitude: {lat}, Longitude: {lng}")
        print("\n")

    # Specify the desired number of groups
    num_groups = 2  # Change this number to the desired number of groups

    # Group coordinates by proximity into the specified number of groups
    grouped_coordinates = group_coordinates_by_distance(latitudes, longitudes, num_groups)

    return grouped_coordinates

if __name__ == "__main__":
    main()
