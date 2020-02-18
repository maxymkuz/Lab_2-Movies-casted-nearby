from parsing import parser
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from folium.features import DivIcon
import time
locator = Nominatim(user_agent="Films nearby")


def get_input():
    """
    Inputs year, latitude and longitude from the user
    :return: ((inr, str, str
    """

    while True:
        try:
            year = int(input("Please enter a year you"
                             " would like to have a map for: "))
            lt, ln = tuple(map(float, input("Please enter your location (for"
                                            "mat: lat, long): ").split(',')))
            break
        except ValueError:
            print("Please enter valid input")
    return year, lt, ln


def get_country(lat, lon):
    """
    Returns a country of these coordnates
    :param lat: float
    :param lon: float
    :return: str
    >>> get_country(33.900002, -119.199997)
    "USA
    """
    location = locator.reverse([lat, lon], language="en-us")
    country = location.raw['address']['country']
    if country == "United States of America" or country == "United States":
        return "USA"
    if country == "United Kingdom":
        return "UK"
    return country


def build_and_display_html(top_10, lat, lon):
    """
    Builds layers with nearest movies distances
    and population of countries, then merges them
    and creates 'map.html file
    :param top_10: list
    :param lat: float
    :param lon: float
    :return: None
    """
    m = folium.Map(location=[lat, lon], zoom_start=7)  # Map object
    film_group = folium.FeatureGroup(name="Markers of film")
    lines_group = folium.FeatureGroup(name="Polylines")
    film_group.add_child(folium.Marker(location=[lat, lon],
                                       popup="Your location",
                                       icon=folium.Icon(icon='cloud',
                                       color='red')))
    for i in range(len(top_10)):
        try:
            film_lat = top_10[i][-3]
            film_lon = top_10[i][-2]
            distance = top_10[i][-1]

            # Adding line layer:
            text = folium.map.Marker(
                [(lat + film_lat) / 2, (lon + film_lon) / 2],
                icon=DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
                    html='<b><div style="font-size: 10pt">{}</div></b>'
                    .format(str(int(distance)) + " km"),
                ))
            lines = folium.PolyLine([(lat, lon), (film_lat, film_lon)],
                                    color="red", weight=2, tooltip="POOOPP",
                                    opacity=0.8)
            lines_group.add_child(text)
            lines_group.add_child(lines)

            films_list = "Here were casted such films as: "
            for j in range(len(top_10[i][0])):
                films_list += top_10[i][0][j] + ", "
                if j >= 5:
                    break

            film_group.add_child(folium.Marker(location=[film_lat, film_lon],
                                               popup=films_list,
                                               icon=folium.Icon(icon='cloud',
                                               icon_color='red')))

        except AttributeError:
            continue

    # Adding third layer:
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('files/world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x:
                                   {'fillColor': 'green'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'orange'
                                   if 10000000 <= x['properties']['POP2005']
                                    < 20000000 else 'red'}))
    m.add_child(fg_pp)
    m.add_child(lines_group)
    m.add_child(film_group)
    m.add_child(folium.LayerControl())
    m.save("map.html")


def find_locations(lat, lon, year):
    """
    Returns a list with 10 or less locations where films were casted
    in particular year, that are neareeest to given coordinates
    :param lat: float
    :param lon: float
    :param year: int
    :return: list
    """
    country = get_country(lat, lon)
    coordinates = parser("files/locations.list", year, country)
    print(coordinates, country, len(coordinates))
    distances = []
    for i in range(len(coordinates)):
        try:
            if 150 <= len(distances) or i >= 200:
                break
            location = locator.geocode(coordinates[i][0])
            film_lat, film_lon = (location.latitude, location.longitude)
            dis = geodesic((film_lat, film_lon), (lat, lon)).km
            distances.append([coordinates[i][1:], film_lat, film_lon, dis])
        except:
            continue

    distances.sort(key=lambda x: x[-1])
    print(len(distances))
    return distances[:10]


if __name__ == "__main__":
    year, lat, lon = get_input()
    print("Map is generating...")
    print("Please wait...")
    distances = find_locations(lat, lon, 2015)
    build_and_display_html(distances, lat, lon,)
    print("Finished. Please have look at the map map.html")
