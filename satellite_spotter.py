import tkinter as tk
from tkinter import ttk
from csv import DictReader
from math import *
from geopy.geocoders import Nominatim
from satellite_tle import fetch_tle_from_celestrak
from skyfield.api import load, EarthSatellite

from geometry import *
from gis import *

re = 6378 # km; radius of Earth (assuming spherical Earth)


def address_func(): 
    ##"Set Address"
    ##(1) print the text entry by the address_label
    address_input =  str(address_box.get())
    address_resp_label.config(text = address_input)
    print("Address: " + address_input)
    ##(2)  find that addresses lat/lon, print by address_latlon_label
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(address_input)
    print("Latitude: " ,loc.latitude,"\nLongtitude: " ,loc.longitude)
    lat, lon = loc.latitude, loc.longitude
    address_latlon_resp_label.config(text = str(lat) +", "+ str(lon))
    print("Address set!")

def time_func():
    time_input = time_box.get()
    time_resp_label.config(text = str(time_input))
    print("Time set!")

def date_func():
    date_input = date_box.get()
    datetime_resp_label.config(text = str(date_input))
    print("Date set!")

## Create a dictionary with Celestrak Satellite catalogue info (downloaded as csv from: https://celestrak.org/satcat/search.php)
satcat_dict = {}
with open('satcat.csv', 'r') as file:
    csv_reader = DictReader(file)
    for row in csv_reader:
        satcat_dict[row[list(row.keys())[0]]] = row

## User select satellite from the list or enter the satelite name
satellite_list = list(satcat_dict.keys())

def create_satellite_dropdown(root_window):
    combo = ttk.Combobox(root_window, value=satellite_list)
    combo.current(0)
    
    def filter_options(event):
        value = event.widget.get()
        if value == '':
            combo['values'] = satellite_list
        else:
            filtered_options = [
                item for item in satellite_list if value.lower() in item.lower()]
            combo['values'] = filtered_options
    
    combo.bind('<KeyRelease>', filter_options)
    return combo

def set_satellite():
    satellite = satellite_dropdown.get()
    print("Selected satellite: " + satellite)
    satellite_resp_label.config(text=satellite)
    print("Satellite set!") 

def geometry_calc():
    ## Grab satellite norad id
    satellite = satellite_dropdown.get()
    norad_id = satcat_dict[satellite]['NORAD_CAT_ID']
    print("Selected satellite: " + satellite + ", " + "NORAD ID: " + norad_id)
    ##grab satellite tle
    tle = fetch_tle_from_celestrak(norad_id)
    ## Parse date/time info
    date = date_box.get()
    time = time_box.get()

    ts = load.timescale()
    year, month, day, hour, minute, second = int(date[0:4]),int(date[4:6]),int(date[6:]), int(time[0:2]),int(time[2:4]), int(time[4:])
    print(year, month, day, hour, minute, second)
    datetime = ts.utc(year, month, day, hour, minute, second)

    ##Skyfield satellite object
    sat_obj = EarthSatellite(tle[1], tle[2], satellite_dropdown.get(), ts)

    ## Satellite position
    position = sat_obj.at(datetime)
    ecef = position.itrf_xyz()##ECEF = Earth centered, Earth frame

    ## Grab the ECEF Cartesian coordinates from the satellite's propagator
    xs, ys, zs = ecef.km[0], ecef.km[1], ecef.km[2]
    ## Convert to spherical (lat/lon) coordinates
    rs = sqrt(xs**2 + ys**2 + zs**2) ## wrt Earth's center
    lat_s = 90 - acos(zs/rs)*(180/pi)
    lon_s = atan2(ys,xs)*180/pi
    alt_s = rs - re
    result = str(lat_s)+", "+ str(lon_s)+", "+ str(alt_s)
    print("Satellite LLA: "+ result)
    satellite_latlon_resp_label.config(text=result)

    ## Calculate the view angle (address-to-satellite view angle; azimuth/elevation)
    # get the address ECEF coords
    LLAa = address_latlon_resp_label.cget("text")
    lat_a, lon_a = LLAa.split(", ") #degrees !
    lat_a, lon_a = float(lat_a), float(lon_a)

    ## check that the user can actually see the satellite!
    LOS, lambda_0a, lambda_0s, lambda_, phia, phis, thetaa, thetas, range_, ela, aza = LOS_geometry(lat_a,lon_a,0, lat_s,lon_s,alt_s) ##address assumed alt = 0 km
    
    ## Look angle calcs
    az = aza*180/pi
    el = ela*180/pi  ## convert to degrees
    # print("LOS, lambda_0a, lambda_0s, lambda_, phia, phis, thetaa, thetas, range_: ", LOS, lambda_0a, lambda_0s, lambda_, phia, phis, thetaa, thetas, range_)

    ## LOS
    LOS_resp_label.config(text=str(LOS))
    ## range to satellite
    range_resp_label.config(text=str(range_))
    ## Viewing az
    az_resp_label.config(text=str(az))
    ## viewing el
    el_resp_label.config(text=str(el))

    print("Calculations complete!")
    

## Main loop
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Satellite Spotter!")
    
    ## Title
    tk.Label(root, text = "Satellite Spotter!").grid(row = 0)

    ## -------- USER INPUTS -----------------------------------
    ##Address text input (Entry/Text)
    tk.Label(root, text = "Enter Address:").grid(row = 1)
    address_box = tk.Entry()
    address_box.grid(row = 1, column = 1)
    address_button = tk.Button(root, text = "Set Address", command = address_func)
    address_button.grid(row = 1, column = 2)

    ##Select satellite (Combobox)
    tk.Label(root, text = "Select Satellite:").grid(row = 2)
    satellite_dropdown = create_satellite_dropdown(root)
    satellite_dropdown.grid(row=2, column=1)
    satellite_button = tk.Button(root, text= "Set Satellite", command = set_satellite)
    satellite_button.grid(row=2, column=2)

    ##Select Time (Entry/Text)
    tk.Label(root, text = "Enter Time (HHMMSS [24-HR]):").grid(row = 3)
    time_box = tk.Entry()
    time_box.grid(row = 3, column = 1)
    time_button = tk.Button(root, text = "Set Time", command = time_func)
    time_button.grid(row = 3, column = 2)

    ##Select Date (Entry)
    tk.Label(root, text = "Enter Date (YYYYMMDD):").grid(row = 4)
    date_box = tk.Entry()
    date_box.grid(row = 4, column = 1)
    date_button = tk.Button(root, text = "Set Date", command = date_func)
    date_button.grid(row = 4, column = 2)

    ## ---------- SET USER RESPONSES -------------------------------------------
    ## section tile
    responses_label = tk.Label(root, text = "Your Entries...")
    responses_label.grid(row = 5)

    ## Address
    address_label = tk.Label(root, text = "Address:")
    address_label.grid(row = 6, column=0)
    address_resp_label = tk.Label(root, text = "")
    address_resp_label.grid(row = 6, column=1)

    ## satellite
    satellite_label = tk.Label(root, text = "Satellite:")
    satellite_label.grid(row = 7, column=0)
    satellite_resp_label = tk.Label(root, text = "")
    satellite_resp_label.grid(row = 7, column=1)

    ##date
    datetime_label = tk.Label(root, text = "Date:")
    datetime_label.grid(row = 8, column=0)
    datetime_resp_label = tk.Label(root, text = "")
    datetime_resp_label.grid(row = 8, column=1)

    ##time
    time_label = tk.Label(root, text = "Time:")
    time_label.grid(row = 9, column=0)
    time_resp_label = tk.Label(root, text = "")
    time_resp_label.grid(row = 9, column=1)

    ## ------------- DISPLAY APP OUTPUTS ------------------------------------------
    ## Calculate button
    calculate_button = tk.Button(root, text="Calculate Az/El", command=geometry_calc)
    calculate_button.grid(row=10, column=1)

    ## section title
    responses_label = tk.Label(root, text = "Satellite Spotter's Results...")
    responses_label.grid(row = 11)

    ## Address lat/lon/alt
    address_latlon_label = tk.Label(root, text = "Address Latitude, Longitude, Altitude (deg/km): ")
    address_latlon_label.grid(row=12)
    address_latlon_resp_label = tk.Label(root, text= "")
    address_latlon_resp_label.grid(row=12, column=1)
    ##satellite lat/lon/alt
    satellite_latlon_label = tk.Label(root, text = "Satellite Latitude, Longitude, Altitude (deg/km): ")
    satellite_latlon_label.grid(row=13)
    satellite_latlon_resp_label = tk.Label(root, text= "")
    satellite_latlon_resp_label.grid(row=13, column=1)

    ## LOS
    LOS_label = tk.Label(root, text= "Line-of-Sight to Satellite: ")
    LOS_label.grid(row = 15)
    LOS_resp_label = tk.Label(root, text= "")
    LOS_resp_label.grid(row=15, column=1)
    ## range to satellite
    range_label = tk.Label(root, text= "Distance to Satellite (km): ")
    range_label.grid(row=16)
    range_resp_label = tk.Label(root, text="")
    range_resp_label.grid(row=16, column=1)
    ## Viewing az
    azimuth_label = tk.Label(root, text= "Viewing Azimuth (deg): ")
    azimuth_label.grid(row=17)
    az_resp_label = tk.Label(root, text="")
    az_resp_label.grid(row=17, column=1)
    ## viewing el
    elevation_label = tk.Label(root, text= "Viewing Elevation (deg): ")
    elevation_label.grid(row=18)
    el_resp_label = tk.Label(root, text="")
    el_resp_label.grid(row=18, column=1)


    ### adding in the map!!
    def _quit():
        root.quit()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", _quit)
    app=Application(root, master=root)
    root.mainloop()
