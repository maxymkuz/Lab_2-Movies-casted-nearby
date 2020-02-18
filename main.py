import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
from folium.features import DivIcon
import time

locator = Nominatim(user_agent="Films nearby")


def parser(location, ipt_year, ipt_country):
    """str -> dict
    Returns a dict with location as a key and title as a value
    """
    res = {}
    with open(location, 'r', encoding="utf-8", errors='ignore') as f:
        for line in f:
            line = line.strip().split('\t')

            for l in range(len(line[0])):
                # Checking if the year is valid
                if line[0][l] == '(' and line[0][l + 1: l + 5].isdigit():
                    year = int(line[0][l + 1: l + 5])

                    if year != ipt_year:
                        break
                    title = line[0][:l]
                    location = line[-2] if line[-1][-1] == ')' else line[-1]
                    if location.endswith(ipt_country):
                        res[location] = res.get(location, []) + [title]
                    break
        lst = [[key] + res[key] for key in res]
        lst.sort(key=lambda x: len(x), reverse=True)
        return lst


def get_input():
    """->(int, float, float)
    Inputs year, latitude and longitude from uset
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
    location = locator.reverse([lat, lon], language="en-us")
    country = location.raw['address']['country']
    if country == "United States of America" or "United States":
        return "USA"
    if country == "United Kingdom":
        return "UK"
    return country


def build_and_display_html(top_10, lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=7)  # Map object
    film_group = folium.FeatureGroup(name="Markers of film")
    lines_group = folium.FeatureGroup(name="Polylines")
    film_group.add_child(folium.Marker(location=[lat, lon],
                                       popup="Your location",
                                       icon=folium.Icon(icon='cloud', color='red')))
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
                    html='<b><div style="font-size: 10pt">{}</div></b>'.format(str(int(distance)) + " km"),
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
                                               icon=folium.Icon(icon='cloud', icon_color='red')))

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
    country = get_country(lat, lon)
    coordinates = parser("files/locations.list", year, country)
    print(coordinates, country, len(coordinates))
    distances = []
    for i in range(len(coordinates)):
        try:
            if 35 <= len(distances) or i >= 100:
                break
            location = locator.geocode(coordinates[i][0])
            film_lat, film_lon = (location.latitude, location.longitude)
            distance = geodesic((film_lat, film_lon), (lat, lon)).km
            print(coordinates[i][0], distance)
            distances.append([coordinates[i][1:], film_lat, film_lon, distance])
        except:
            continue

    distances.sort(key=lambda x: x[-1])
    print(len(distances))
    return distances[:10]


distances = find_locations(33.900002, -119.199997, 2015)
build_and_display_html(distances, 33.900002, -119.199997)
