import requests

# Replace with your MapQuest API Key
MAPQUEST_API_KEY = 'C3LFx5vksRYoxuZZL9IFtiItNVAL1SLH'


def optimize_routes(bus_stops, num_buses):
    # Divide the stops into equal chunks for each bus
    chunks = [bus_stops[i:i + len(bus_stops) // num_buses] for i in
              range(0, len(bus_stops), len(bus_stops) // num_buses)]

    optimized_routes = []

    for i, chunk in enumerate(chunks):
        bus_name = f"Bus {i + 1}"

        # Set the starting point as the last stop of the previous bus (if not the first bus)
        if i > 0:
            starting_point = chunks[i - 1][-1]
        else:
            starting_point = None

        # Request optimized directions for the bus
        route = get_optimized_route(starting_point, chunk)

        # Append the route to the list of optimized routes
        optimized_routes.append((bus_name, route))

    return optimized_routes


def get_optimized_route(starting_point, stops):
    # Prepare the request data for MapQuest Directions API
    request_data = {
        'key': MAPQUEST_API_KEY,
        'from': starting_point,
        'to': '|'.join(stops),
        'routeType': 'shortest',
        'doReverseGeocode': 'false',
        'ambiguities': 'ignore',
    }

    # Make the API request
    response = requests.get('http://www.mapquestapi.com/directions/v2/route', params=request_data)

    if response.status_code == 200:
        data = response.json()
        if 'route' in data and 'legs' in data['route'] and len(data['route']['legs']) > 0:
            # Extract and return the maneuvers for the first leg of the route
            return data['route']['legs'][0]['maneuvers']
        else:
            print(f"Error: Unable to fetch route for stops {stops}")
    else:
        print(f"Error: Unable to fetch route for stops {stops}")

    return []


def done(bus_stops, num_buses):
    optimized_routes = optimize_routes(bus_stops, num_buses)

    # Display the optimized routes for each bus
    for bus_name, route in optimized_routes:
        print(f"{bus_name} Route:")
        for step in route:
            print(step['narrative'])
        print("\n")
