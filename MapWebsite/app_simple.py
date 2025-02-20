from flask import Flask, request, render_template
import folium
from folium.plugins import Draw
from geopy import Nominatim

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():

    # Create the geolocator so we can find the user's location.
    geolocator = Nominatim(user_agent = "WalkingTour")

    # Set defaults.
    location = "Providence RI"
    providence = geolocator.geocode(location)
    latitude = providence.latitude
    longitude = providence.longitude
    message = ""

    # Get lat, long from the user's location or the default.
    if request.method == "POST":
        location = request.form.get("location")
        if location:
            geo_location = geolocator.geocode(location)
            if geo_location:
                latitude = geo_location.latitude
                longitude = geo_location.longitude
            else:
                message = "Couldn't find " + location
            
        
    # Create a Folium map centered at the given coordinates
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    Draw(export=True, filename="my_data.geojson").add_to(m)

    # Render map as HTML
    map_html = m._repr_html_()

    return render_template('index_simple.html', map_html=map_html, location=location,
                           message = message)

if __name__ == "__main__":
    app.run(debug=True)
