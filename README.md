## Parking-Violation-based-on-Zip-Code### Parking Violations Based on Zip Codes of NYC

A python code that allows for the compliation of Parking Violations and displays it for each individual Zip Code in New York City. Planned to include a simple input that allows for users to specify which street they're interested in to further return the Parking Violations in proportion to the Average Daily Traffic Count.

### Data Visualization / Paragraph

A image of the generated HTML file for the created visualization of NYC organized by Zip Code. It contain's the Zip Code of the highlighted area as well as the Parking Violations 
in that area as a caption/popup as you hover over it. It also includes a marker that will be generated at the Zip Code corresponding to the area the entered street given is. The Marker contains data on the parking violations in that area as a ratio to the Average Daily Traffic count of the same street. The data is sourced from open source Parking violation data and Traffic data. Methods used include APIs with Geopy, Pandas, Regex, SQL, Folium, as well as Json/Geojson

![Image](https://user-images.githubusercontent.com/32392170/145610406-3f62885e-ce04-435d-b518-e98e46b9cee0.png)

### Data

Traffic Volume Data from NYC Open Data
https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-2014-2019-/ertz-hr4r

Parking Violation Data from NYC Open Data
https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2022/pvqr-7yc4/data

NYC Zip Code Geojson File
https://jsspina.carto.com/tables/nyc_zip_code_tabulation_areas_polygons/public/map

### Techinques 
 
Geopy was used to parse and retrieve Zip code and address data. Pandas was used for data access and management. Regex and SQL was both used for cleaning parsing data fields to be used together. Json and Geojson files were used for map and visualization on the folium map. Default methods were also used to avoid crashes and errors. 

![pepe](https://user-images.githubusercontent.com/32392170/145614312-94f90833-50a6-4cbd-8afe-a985a283ddec.png)


### PROBLEM

THIS CODE CURRERNTLY DOES NOT WORK ON MASSIVE FILES, as geopy will stop allowing you to request calls from its URL. VERY minimally working product atm...

### Citations

https://jsspina.carto.com/tables/nyc_zip_code_tabulation_areas_polygons/public/map
https://pandas.pydata.org/
https://www.python-graph-gallery.com/map-read-geojson-with-python-geopandas
https://medium.com/@h4k1m0u/plot-a-geojson-map-using-geopandas-be89e7a0b93b
https://python-visualization.github.io/folium/quickstart.html
https://towardsdatascience.com/using-folium-to-generate-choropleth-map-with-customised-tooltips-12e4cec42af2
https://gis.stackexchange.com/questions/392531/modify-geojson-tooltip-format-when-using-folium-to-produce-a-map
https://python-visualization.github.io/folium/quickstart.html
https://chriswhong.github.io/plutoplus/#
https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-2014-2019-/ertz-hr4r
https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2022/pvqr-7yc4/data
https://dmv.ny.gov/statistic/2018reginforce-web.pdf
https://stackoverflow.com/questions/55178112/update-values-in-geojson-file-in-python
https://stackoverflow.com/questions/35108199/python-which-is-a-fast-way-to-find-index-in-pandas-dataframe
https://stackoverflow.com/questions/42753745/how-can-i-parse-geojson-with-python

## Scuffed Honestly but do give me any feedback you can!

THANKS FOR LOOKING AT MY PROJECT!
