from flask import Flask, request, render_template, jsonify
import folium
from folium.plugins import Draw
from geopy import distance
from geopy import Nominatim
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Set defaults.
    geolocator = Nominatim(user_agent="WalkingTour")
    default_location = "Providence RI"
    default_geo = geolocator.geocode(default_location)
    location = default_location
    latitude = default_geo.latitude
    longitude = default_geo.longitude
    message = ""
    instructions = "Export your map and press 'Calculate Route distance' to see your walking route length."

    # If there's a location and the user has pressed the Update Map button,
    # update the map and log the data.
    if request.method == "POST" and "location" in request.form:
        location = request.form["location"]
        geo_location = geolocator.geocode(location)
        if geo_location:
            latitude, longitude = geo_location.latitude, geo_location.longitude
        else:
            message = "Couldn't find " + location

    # Now generate the map.
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    Draw(export=True, filename="my_data.geojson").add_to(m)
    map_html = m._repr_html_()  

    return render_template("index.html", location=location, message=message,
                           instructions=instructions, map_html=map_html)

@app.route("/calculate_route", methods=["GET"])
def calculate_route():
    """ Reads the exported route file and calculates the distance without reloading the page. """
    try:
        with open("my_data.geojson") as f:
            data = json.load(f)
            # Catch these exceptions and print the message if
            # debugging, but otherwise we'll just print a generic
            # message.
            if "features" not in data or not data["features"]:
                raise ValueError("GeoJSON file has no features.")
            coordinates = data["features"][0]["geometry"]["coordinates"]
            if len(coordinates) < 2:
                raise ValueError("Not enough coordinates to calculate distance.")
            
            # Compute the distance between all the coordinate pairs.
            total_length = 0
            for i in range(len(coordinates) - 1):
                total_length  += distance.distance([coordinates[i][1], coordinates[i][0]],
                                                   [coordinates[i + 1][1], coordinates[i+1][0]]).miles
            return jsonify({"route": f"Your route is {total_length:.2f} miles."})

    except FileNotFoundError:
        return jsonify({"error": "GeoJSON file not found. Please export your route."})
    except Exception as e:
        return jsonify({"error": f"Something went wrong"})



if __name__ == "__main__":
    app.run(debug=True)
