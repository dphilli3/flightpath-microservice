from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/flightpath', methods=['POST'])
def get_flight_path():
    flights = request.json.get('flights', [])
    if not flights:
        return jsonify({"error": "No flights provided"}), 400
    
    try:
        sorted_path = sort_flights(flights)
        return jsonify({"flight_path": sorted_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def sort_flights(flights):
    # Create a map to hold the next destination for each source
    flight_map = {source: destination for source, destination in flights}
    
    # Find the start of the flight path
    all_sources = set(flight_map.keys())
    all_destinations = set(flight_map.values())
    start = list(all_sources - all_destinations)[0]
    
    # Build the sorted flight path
    sorted_path = [start]
    while start in flight_map:
        next_destination = flight_map[start]
        sorted_path.append(next_destination)
        start = next_destination
    
    return sorted_path

if __name__ == '__main__':
    app.run(debug=True)
