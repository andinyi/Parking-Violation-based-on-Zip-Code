'''
Handy Ni
Parking Mapping and Data handling file for the time being
Title: Parking Violation Mapping By Zip Code
URL: https://andinyi.github.io/Parking-Violation-based-on-Zip-Code/
Resources: https://pandas.pydata.org/, https://www.python-graph-gallery.com/map-read-geojson-with-python-geopandas, https://medium.com/@h4k1m0u/plot-a-geojson-map-using-geopandas-be89e7a0b93b, https://python-visualization.github.io/folium/quickstart.html, https://towardsdatascience.com/using-folium-to-generate-choropleth-map-with-customised-tooltips-12e4cec42af2
https://gis.stackexchange.com/questions/392531/modify-geojson-tooltip-format-when-using-folium-to-produce-a-map, https://python-visualization.github.io/folium/quickstart.html, https://chriswhong.github.io/plutoplus/#, https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-2014-2019-/ertz-hr4r, https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2022/pvqr-7yc4/data
https://dmv.ny.gov/statistic/2018reginforce-web.pdf, https://stackoverflow.com/questions/55178112/update-values-in-geojson-file-in-python, https://stackoverflow.com/questions/35108199/python-which-is-a-fast-way-to-find-index-in-pandas-dataframe, https://stackoverflow.com/questions/42753745/how-can-i-parse-geojson-with-python
'''

from folium.features import GeoJsonTooltip
import numpy as np
import pandas as pd
from pandas.core.dtypes.missing import na_value_for_dtype
import pandasql as psql
import matplotlib.pyplot as plt
import geojson as gs
import geopandas as gpd
import datetime as dt
import folium
import json 
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter


def roundTime(df, timeCol): #time rounding function
    tmp = ''
    for i in range(len(df)):
        tmp = df.loc[i, timeCol]
        tmp = tmp[-1:]
        x = round(int(df.loc[i, timeCol][:-1]), -2)
        df.loc[i, timeCol] = str(x) + tmp
    return df

def streetNameDf(df): #returns a df containing occurences of parking violations per street 
    query = 'SELECT "Street Name", COUNT("Street Name") as Count FROM df GROUP BY "Street Name"'
    outDf = psql.sqldf(query)
    return outDf

def countOfUniqueIds(df): #counts unique IDs not ending up being used in the final product
    query = 'SELECT COUNT(DISTINCT("Plate ID")) FROM df'
    outDf = psql.sqldf(query)
    return outDf

def cleanStreet(str): #cleans street names for usage
    str = str.upper()
    if('AVENUE' in str):
        str = str.replace('AVENUE', 'AVE')
    if('STREET' in str):
        str = str.replace('STREET', 'ST')
    str = (re.compile(r"(?<=\d)(ND|RD|TH)").sub("", str))

    return str

def pVfromStreet(df, streetname): #Returns all the rows where StreetName = streetname as a dataframe used for counting Parking Violations upon a street input
    streetname = streetname.upper()
    out = df[df['Street Name'] == streetname]
    return out

def returnZipCode(streetname): #Returns a zipcode when given an address (GEOPY does not like when i request too many times and now my whole project cant go further because with it being too big it wont let me run the zip lookup sadge)
    geolocator = Nominatim(user_agent="Parking violations")
    place = streetname
    place = place + ' NYC'
    RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=0)
    location = geolocator.geocode(place)   
    if(location is None):
        return
    data = location.raw
    out_data = data['display_name'].split()
    if((out_data[-3])[:5].isdecimal()):
        return (out_data[-3])[:5]
    else: 
        return

def zipSeries(df): ##returns all zips in a series/ Cleaned
    cp = pd.Series(dtype=object)
    cp = df['Street Name']
    cp = cp.apply(returnZipCode)
    cp = cp.dropna()
    return cp

def returnPercentDf(zip):#returns a zip code df with counts for parsing and mapping 
    df = pd.DataFrame()
    df['Zip Code'] = zip
    query = 'SELECT "Zip Code", COUNT("Zip Code") as "Parking Violations Count" FROM df GROUP BY "Zip Code"'
    outDf = psql.sqldf(query)
    return outDf

def combineDups(df): #groupby and sums up
    df = df.groupby(['Roadway Name']).sum()
    return df

def makeTrafficSumDf(df): #traffic sum dataframe 
    df1 = df.sum(axis=1, skipna=True)
    return df1

def getCoords(geojson, zipcode): #parses and returns me a zipcode to use for coordinates for marker
    singular = geojson['postalcode']
    arr = []
    lat = []
    long = []
    for i in range(len(singular)):
        if(str(singular[i]) == str(zipcode)):
            new = str(geojson['geometry'][i])
            new = new.replace('MULTIPOLYGON ', '')
            new = new.replace('(', '')
            new = new.replace(')', '')
            new = new.replace(',', '')
            arr = new.split(' ')
            break
    for i in range(len(arr)):
        if(i % 2 != 0):
            lat.append(np.double(arr[i]))
        else:
            long.append(np.double(arr[i]))
    if(len(lat) == 0 or len(long) == 0):
        return 40.7128, -74.0060
    lat = sum(lat)/len(lat)
    long = sum(long)/len(long)
    return lat, long 

def applyToolTips(df, geojson): #adds tooltips to the map
    tooltip = []
    singular = geojson['postalcode']
    zip = df['Zip Code'].apply(str)
    for i in singular:
        bool1 = zip.str.contains(i)
        if(bool1.sum() > 0):
            #print(df.loc[df['Zip Code'] == i])
            tooltip.append(df.loc[df['Zip Code'] == i, 'Parking Violations Count'].iloc[0])
        else:
            tooltip.append(np.nan)
    
    geojson['tooltip'] = tooltip

    return geojson 

def makeZipcodeMap(data): #makes the map
    map = folium.Map(location=[40.693943, -73.985880], default_zoom_start=15)
    choropleth = folium.Choropleth(
        geo_data=data,
        name="cholorpleth",
        fill_opacity=0.7,
        line_opacity=0.4,
        highlight=True,
        fill_color='#7851A9',
        key_on="features.properties.postalcode",
    ).add_to(map)
    #for i in range(len(df)):=
    choropleth.geojson.add_child(GeoJsonTooltip(['po_name', 'postalcode', 'tooltip'], aliases=['Name (If available): ', 'Zip Code: ', 'Parking Violation Count: '], labels=True))
    return map



#folium.Marker(location=[40.69153, -73.95605], popup="pp").add_to(map)

# Handling Inputs / Testing Inputs

# <<< INITIALIZING DATA >>>
x = input('\033[1;32;40mWould you like to run default (0) or single out a street (1)?\n\033[0;37;40m')
if(x == '0'): #if choosing x 
    PViol = pd.read_csv('Pviol.csv') #reads in small version of Pviol.csv
    query = 'SELECT "Street Name", "Issue Date", "Plate Type" FROM PViol' #gets what we need, does not import anything more than what we need 
    parkingDf = psql.sqldf(query)
    Pviol = 0 #clears Pviol (Privacy Concerns)  
    data = gpd.read_file('Zip_code.geojson') #reads in geojson file for zipcodes
    parkingDf['Street Name'] = parkingDf['Street Name'].apply(cleanStreet) #cleaning streets
    makeZipDf = pd.read_csv('zipCodes.csv') #to avoid having to run the zip code compiling processing but the process is commentented out 
    makeZipDf['Zip Code'] = makeZipDf['Zip Code'].apply(str) #cleans
    #zipCodes = zipSeries(parkingDf)
    #makeZipDf = returnPercentDf(zipCodes)
    data = applyToolTips(makeZipDf, data)
    map = makeZipcodeMap(data)
    map.save('map.html')

elif(x == '1'):
    y = input('\033[1;32;40mPlease enter the street you are interested in\n\033[0;37;40m') #if want to input street 
    y = cleanStreet(y) #cleans 
    PViol = pd.read_csv('Pviol.csv')
    query = 'SELECT "Street Name", "Issue Date", "Plate Type" FROM PViol'
    parkingDf = psql.sqldf(query)  
    data = gpd.read_file('Zip_code.geojson')
    Pviol = 0 #clears Pviol (Privacy Concerns)
    parkingDf['Street Name'] = parkingDf['Street Name'].apply(cleanStreet) #cleans

    traffic = pd.read_csv('TVC.csv') #reads in lesser traffic data
    traffic = traffic.drop(columns=['ID', 'Segment ID', 'Direction', 'Date']) #getting rid of data we dont need
    traffic['Roadway Name'] = traffic['Roadway Name'].apply(cleanStreet) #cleans
    traffic = combineDups(traffic) #combines dups and sums it up
    sumOfTraffic = makeTrafficSumDf(traffic) #creates a dataframe with traffic sums to work with 
    if(y in sumOfTraffic.index):
        #print(sumOfTraffic.loc[y]) #use for coordinates on marker
        parkingDf = streetNameDf(parkingDf) 
        r1 = 0 #base case 0 
        if(parkingDf['Street Name'].str.contains(y).any()): #if any of the Street name contain y
            r1 = parkingDf.loc[parkingDf['Street Name'] == y, 'Count'].iloc[0] #returns the count of traffic
        ratio = "Street Name:" + y + "--------Parking Violation: " + str(r1) + " " + "--------Daily Average Traffic: "  +  str(sumOfTraffic.loc[y])#gets our ratio and returns it as a string for using it in our tooltip separated by ------- 
        tmp = y 
        postal = returnZipCode(tmp) #gets our zipcode 
        if(returnZipCode(tmp) == None): #gets us the marker coords using zipcode
            print('Could not fetch Zip Code, Defaulting to NYC coords') #default if zipcode fetch fails
            lat, long = 40.7128, -74.0060 #base case coords for nyc 
            postal = 10007 #base case zipcode
        else:   
            lat, long = getCoords(data, postal) #postal coords
        makeZipDf = pd.read_csv('zipCodes.csv') #to avoid having to run the zip code compiling processing but the process is commentented out 
        makeZipDf['Zip Code'] = makeZipDf['Zip Code'].apply(str) #cleans
        #zipCodes = zipSeries(parkingDf)
        #makeZipDf = returnPercentDf(zipCodes)
        data = applyToolTips(makeZipDf, data)
        map = makeZipcodeMap(data)
        folium.Marker(location=[lat, long], popup=ratio).add_to(map)
        map.save('map.html')

    else: 
        print('\033[1;33;40mStreet not found in dataset, defaulting to default map print\n\033[0;37;40m')
        #zipCodes = zipSeries(parkingDf)
        #makeZipDf = returnPercentDf(zipCodes)
        makeZipDf = pd.read_csv('zipCodes.csv')
        makeZipDf['Zip Code'] = makeZipDf['Zip Code'].apply(str)
        data = applyToolTips(makeZipDf, data)
        map = makeZipcodeMap(data)
        map.save('map.html')

    #zipCodes = zipSeries(parkingDf)
    #makeZipDf = returnPercentDf(zipCodes)
    #-----------------------------------------------------
    #makeZipDf = pd.read_csv('zipCodes.csv')
    #makeZipDf['Zip Code'] = makeZipDf['Zip Code'].apply(str)
    #data = applyToolTips(makeZipDf, data)
    #map = makeZipcodeMap(data)
    #map.save('map.html')

    




#parkingDf = roundTime(parkingDf, 'Violation Time')
#countOfStreets = streetNameDf(parkingDf

#<<< FUNCTION CALLS >>>
#parkingDf = cleanStreetHelper(parkingDf)
#zipCodes = zipSeries(parkingDf)


#makeZipDf = returnPercentDf(zipCodes)
#makeZipDf = pd.read_csv('zipCodes.csv')
#makeZipDf['Zip Code'] = makeZipDf['Zip Code'].apply(str)
#data = applyToolTips(makeZipDf, data)

#makeZipcodeMap(data).save('map.html')






