## libraries
from csv import reader, DictReader
from math import *
from satellite_tle import fetch_tle_from_celestrak
import tkinter as tk
from tkinter import ttk
from geopy.geocoders import Nominatim


## =================================================================================================================================================================================
## Create a dictionary with Celestrak Satellite catalogue info (downloaded as csv from: https://celestrak.org/satcat/search.php)
satcat_dict = {}
with open('satcat.csv', 'r') as file:
    csv_reader = DictReader(file)
    for row in csv_reader:
        satcat_dict[row[list(row.keys())[0]]] = row

## User select satellite from the list or enter the satelite name
sat_payload_list = list(satcat_dict.keys())

def create_satellite_dropdown(parent):
    combo = ttk.Combobox(parent, values=sat_payload_list)
    combo.current(0)  # Set default value

    def filter_options(event):
        value = event.widget.get()
        if value == '':
            combo['values'] = sat_payload_list
        else:
            filtered_options = [
                item for item in sat_payload_list if value.lower() in item.lower()
            ]
            combo['values'] = filtered_options
    
    combo.bind('<KeyRelease>', filter_options)
    return combo

##
def get_norad_id(): #what happens when the user selects a satellite from the drop down
    selected_key = dropdown.get()
    norad_id = satcat_dict[selected_key]['NORAD_CAT_ID']
    print(f"Selected: {selected_key}, Value: {norad_id}")

## User types in their address; returns a lat/lon
def get_user_latlon():
    address = txtbox.get()
    print("Address: %s" % (txtbox.get()))
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(txtbox.get())
    print("latitude:" ,loc.latitude,"\nlongtitude:" ,loc.longitude)
    lat, lon = loc.latitude, loc.longitude
    return address, lat, lon 
    
## Geometry calcs
def geometry_calculator(address):
    if address == 1:
        print("some stuff")
    else:
        print("ha!")




if __name__ == '__main__':
    root = tk.Tk()
    root.title("Satellite Finder!")

    tk.Label(root, text="Address").grid(row=0)
    txtbox = tk.Entry(root) ## get() -- address string
    txtbox.grid(row=0, column=1)
    tk.Button(root, text='Set Address', command=get_user_latlon).grid(row=3, column=1, sticky=tk.W, pady=4)

    dropdown = create_satellite_dropdown(root) ## get() -- satellite dict
    dropdown.grid(row=1,column=1)
    
    select_button = tk.Button(root, text="Select Satellite", command=get_norad_id)
    select_button.grid(row=2,column=1)

    calculate_button = tk.Button(root, text = "Calculate Az/El", command=geometry_calculator).grid(row=4, column=1, sticky=tk.W, pady=4)

    root.mainloop()


