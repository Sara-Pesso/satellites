import earthpy as ep
import geopandas as gp
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation
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
    try: 
        geolocator = Nominatim(user_agent="my_user_agent")
        loc = geolocator.geocode(address_input)
        print("Latitude: " ,loc.latitude,"\nLongtitude: " ,loc.longitude)
        lat, lon = loc.latitude, loc.longitude
        print("Used GeoPy for address LLA")
    except:
        clean_str = address_input.rstrip()
        zipcode = clean_str[-5:]
        LL = ZipcodeLLA('us', zipcode)
        lat,lon = LL['lat'], LL['lon']
        print("Used Zipcode for LLA")

    address_latlon_resp_label.config(text = str(lat) +", "+ str(lon))
    print("Address set!")

def stime_func():
    stime_input = stime_box.get()
    stime_resp_label.config(text = str(stime_input))
    print("Start Time set!")

def sdate_func():
    sdate_input = sdate_box.get()
    sdatetime_resp_label.config(text = str(sdate_input))
    print("Start Date set!")

def etime_func():
    etime_input = etime_box.get()
    etime_resp_label.config(text = str(etime_input))
    print("End Time set!")

def edate_func():
    edate_input = edate_box.get()
    edatetime_resp_label.config(text = str(edate_input))
    print("End Date set!")

def iter_func():
    iter_input = iter_box.get()
    iter_resp_label.config(text = str(iter_input))
    print("Time Step (s) set!")

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
    sdate = sdate_box.get()
    stime = stime_box.get()

    ts = load.timescale()
    year, month, day, hour, minute, second = int(sdate[0:4]),int(sdate[4:6]),int(sdate[6:]), int(stime[0:2]),int(stime[2:4]), int(stime[4:])
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

def view_window():
    ## Grab satellite norad id
    satellite = satellite_dropdown.get()
    norad_id = satcat_dict[satellite]['NORAD_CAT_ID']
    print("Selected satellite: " + satellite + ", " + "NORAD ID: " + norad_id)
    ##grab satellite tle
    tle = fetch_tle_from_celestrak(norad_id)
    ## Parse date/time info
    sdate = sdate_box.get()
    stime = stime_box.get()
    edate = edate_box.get()
    etime = etime_box.get()

    ts = load.timescale()
    
    syear, smonth, sday, shour, sminute, ssecond = int(sdate[0:4]),int(sdate[4:6]),int(sdate[6:]), int(stime[0:2]),int(stime[2:4]), int(stime[4:])
    eyear, emonth, eday, ehour, eminute, esecond = int(edate[0:4]),int(edate[4:6]),int(edate[6:]), int(etime[0:2]),int(etime[2:4]), int(etime[4:])

    sdatetime = ts.utc(syear, smonth, sday, shour, sminute, ssecond)
    edatetime = ts.utc(eyear, emonth, eday, ehour, eminute, esecond)

    total_interval = round((edatetime-sdatetime)*24*60*60)

    ##Skyfield satellite object
    sat_obj = EarthSatellite(tle[1], tle[2], satellite_dropdown.get(), ts)

    geometry_info_dict = {}
    satellite_position_dict = {}
    for s in range(0,total_interval, int(iter_box.get())): #from 0 (start interval) - end of interval, iterating by x sec.
        ## Satellite position at interval time s
        position = sat_obj.at(ts.utc(syear, smonth, sday, shour, sminute, ssecond+s))
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

        satellite_position_dict[s] = (lat_s,lon_s,alt_s,xs,ys,zs)
        # print(satellite_position_dict)

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

        geometry_info_dict[s] = (LOS, lambda_0a, lambda_0s, lambda_, phia, phis, thetaa, thetas, range_, ela, aza)
        # print(geometry_info_dict)

        if s == 0: #only display for time 0 (for now! TODO: make it so the first time info the satellite is visible during the user defined interval is displayed)
            satellite_latlon_resp_label.config(text=result)
            ## LOS
            LOS_resp_label.config(text=str(LOS))
            ## range to satellite
            range_resp_label.config(text=str(range_))
            ## Viewing az
            az_resp_label.config(text=str(az))
            ## viewing el
            el_resp_label.config(text=str(el))

        print("Calculations complete!")
        #TODO: if s(0) LOS==true, working backwards to find the true start of the view window
        #TODO: if (s(e)) LOS==true, continue iterating to find true end of the view window
        #TODO: maybe remove end date/time user input? Just find the closest view window to the give date/time
    
    ### adding in the map to tkinter gui!!
    SatelliteAnimation(geometry_info_dict, satellite_position_dict, lat_a, lon_a, time_step=iter_box.get())
## Main loop
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Satellite Watcher!")
    
    ## Title
    tk.Label(root, text = "Satellite Watcher!").grid(row = 0)

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

    ##Select Start Time (Entry/Text)
    tk.Label(root, text = "Enter Start Time (HHMMSS [24-HR]):").grid(row = 3)
    stime_box = tk.Entry()
    stime_box.grid(row = 3, column = 1)
    stime_button = tk.Button(root, text = "Set Start Time", command = stime_func)
    stime_button.grid(row = 3, column = 2)

    ##Select Start Date (Entry)
    tk.Label(root, text = "Enter Start Date (YYYYMMDD):").grid(row = 4)
    sdate_box = tk.Entry()
    sdate_box.grid(row = 4, column = 1)
    sdate_button = tk.Button(root, text = "Set Start Date", command = sdate_func)
    sdate_button.grid(row = 4, column = 2)

    ##Select End Time (Entry/Text)
    tk.Label(root, text = "Enter End Time (HHMMSS [24-HR]):").grid(row = 5)
    etime_box = tk.Entry()
    etime_box.grid(row = 5, column = 1)
    etime_button = tk.Button(root, text = "Set End Time", command = etime_func)
    etime_button.grid(row = 5, column = 2)

    ##Select End Date (Entry)
    tk.Label(root, text = "Enter End Date (YYYYMMDD):").grid(row = 6)
    edate_box = tk.Entry()
    edate_box.grid(row = 6, column = 1)
    edate_button = tk.Button(root, text = "Set End Date", command = edate_func)
    edate_button.grid(row = 6, column = 2)

    ##Select Time Step (s) (Entry/Text)
    tk.Label(root, text = "Enter Time Step (seconds):").grid(row = 7)
    iter_box = tk.Entry()
    iter_box.grid(row = 7, column = 1)
    iter_button = tk.Button(root, text = "Set Time Step", command = iter_func)
    iter_button.grid(row = 7, column = 2)

    ## ---------- SET USER RESPONSES -------------------------------------------
    ## section tile
    responses_label = tk.Label(root, text = "Your Entries...")
    responses_label.grid(row = 8)

    ## Address
    address_label = tk.Label(root, text = "Address:")
    address_label.grid(row = 9, column=0)
    address_resp_label = tk.Label(root, text = "")
    address_resp_label.grid(row = 9, column=1)

    ## satellite
    satellite_label = tk.Label(root, text = "Satellite:")
    satellite_label.grid(row = 10, column=0)
    satellite_resp_label = tk.Label(root, text = "")
    satellite_resp_label.grid(row = 10, column=1)

    ##start date
    sdatetime_label = tk.Label(root, text = "Start Date:")
    sdatetime_label.grid(row = 11, column=0)
    sdatetime_resp_label = tk.Label(root, text = "")
    sdatetime_resp_label.grid(row = 11, column=1)

    ##start time
    stime_label = tk.Label(root, text = "Start Time:")
    stime_label.grid(row = 12, column=0)
    stime_resp_label = tk.Label(root, text = "")
    stime_resp_label.grid(row = 12, column=1)

    ##end date
    edatetime_label = tk.Label(root, text = "End Date:")
    edatetime_label.grid(row = 13, column=0)
    edatetime_resp_label = tk.Label(root, text = "")
    edatetime_resp_label.grid(row = 13, column=1)

    ##end time
    etime_label = tk.Label(root, text = "End Time:")
    etime_label.grid(row = 14, column=0)
    etime_resp_label = tk.Label(root, text = "")
    etime_resp_label.grid(row = 14, column=1)

    ##time step (seconds)
    iter_label = tk.Label(root, text = "Time Step (seconds):")
    iter_label.grid(row = 15, column=0)
    iter_resp_label = tk.Label(root, text = "")
    iter_resp_label.grid(row = 15, column=1)

    ## ------------- DISPLAY APP OUTPUTS ------------------------------------------
    ## Calculate button
    calculate_button = tk.Button(root, text="Calculate Az/El", command=view_window)
    calculate_button.grid(row=16, column=1)

    ## section title
    responses_label = tk.Label(root, text = "Satellite Watcher's Results...")
    responses_label.grid(row = 18)

    ## Address lat/lon/alt
    address_latlon_label = tk.Label(root, text = "Address Latitude, Longitude, Altitude (deg/km): ")
    address_latlon_label.grid(row=19)
    address_latlon_resp_label = tk.Label(root, text= "")
    address_latlon_resp_label.grid(row=19, column=1)
    ##satellite lat/lon/alt
    satellite_latlon_label = tk.Label(root, text = "Satellite Latitude, Longitude, Altitude (deg/km): ")
    satellite_latlon_label.grid(row=20)
    satellite_latlon_resp_label = tk.Label(root, text= "")
    satellite_latlon_resp_label.grid(row=20, column=1)

    ## LOS
    LOS_label = tk.Label(root, text= "Line-of-Sight to Satellite: ")
    LOS_label.grid(row = 21)
    LOS_resp_label = tk.Label(root, text= "")
    LOS_resp_label.grid(row=21, column=1)
    ## range to satellite
    range_label = tk.Label(root, text= "Distance to Satellite (km): ")
    range_label.grid(row=22)
    range_resp_label = tk.Label(root, text="")
    range_resp_label.grid(row=22, column=1)
    ## Viewing az
    azimuth_label = tk.Label(root, text= "Viewing Azimuth (deg): ")
    azimuth_label.grid(row=23)
    az_resp_label = tk.Label(root, text="")
    az_resp_label.grid(row=23, column=1)
    ## viewing el
    elevation_label = tk.Label(root, text= "Viewing Elevation (deg): ")
    elevation_label.grid(row=24)
    el_resp_label = tk.Label(root, text="")
    el_resp_label.grid(row=24, column=1)
    
    root.mainloop()