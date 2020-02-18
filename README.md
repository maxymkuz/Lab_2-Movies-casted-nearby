# Movies casted nearby

### This reository is written on Python programming language to help curious people to examine the locations of movies that were casted in a given year better and with ease.

> Two Python modules are used in this repository(geopy and folum), so in order to successfully run the main.py, you need do install them:

```bash
pip3 install geopy

pip3 install folium
```
* The program returns an html file, where are marks of movie locations and their titles, distances to them and country population
* There is the option to include or exclude some of three layers on hte top right panel of html-page
    1. Layer with markers of 10 or less films nearby in that country in that particular year
    2. Layer with the distances to all those markers
    3. Layer, which reflects the population of all countries and paints them with an appropriate colors

#### Structure of html file that main module returns:
```HTML
<!DOCTYPE html> -- defines which document type is it
<head> -- Different information about the title of map and the map itself
<body> -- the main part of the html-file
<link> -- Makes a link to an external resources
<script> -- Info about script, usually written in Python or JS
<div> -- literally is translated as division
```

### Conclusion:
The information, given by this map could be usefull to almost anybody, but esecially useful for some Data Scientists who want to better analyze the tendentions in where movies are cast and how they differ in different counties, or, even, regions. Using third layer user can instantly see the corelations between country population and movies casted in it's regions.