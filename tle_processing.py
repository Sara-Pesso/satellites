## USER INPUTS
tle_csv = 'starlink_20250415.csv'
#epoch
year = 2025
month = 4
day = 18
hour = 2
minute = 3
second = 25
# simulation duration, in seconds
dur_s = 10
# interval length, seconds
int_s = 1

##=====================================================================##
## Import the necessary libraries
from skyfield.api import load, EarthSatellite
from csv import reader
from math import *

## Constants
re = 6378 ## Radius of the Earth (assuming spherical Earth; ignore flattening at the poles)

## Format the constellation's TLEs from those listed in the user's CSV file
tle_dict = {}
with open(tle_csv, newline = '') as csvfile:
        tle_sep = reader(csvfile, delimiter= ' ')
        c = 0
        for line in tle_sep:
            tle_line = " ".join(i for i in line)
            if c % 3 == 0:
                    sat = " ".join(tle_line.split())
                    tle_dict[sat] = {}
            if c % 3 == 1:
                    tle_dict[sat]['s'] = tle_line
            if c % 3 == 2:
                    tle_dict[sat]['t'] = tle_line
            c += 1

ts = load.timescale()
print(ts)

## Pre-calculate the positional information for each satellite, as a function of time
satloc = {}
for sat in tle_dict.keys():
    satloc[sat] = {}
    print(sat)
    for t in range(0, dur_s, int_s):
        satellite = EarthSatellite(tle_dict[sat]['s'], tle_dict[sat]['t'], sat, ts)
        time = ts.utc(year, month, day, hour, minute, second + t) ## Format the UTC time from the given UTC date
        position = satellite.at(time)
        ecef = position.itrf_xyz() ##ECEF = Earth centered, Earth frame

        ## Grab the ECEF Cartesian coordinates from the propagators
        x, y, z = ecef.km[0], ecef.km[1], ecef.km[2]

        ## Convert to spherical (lat/lon) coordinates
        rs = sqrt(x**2 + y**2 + z**2) ## wrt Earth's center
        lat = 90 - acos(z/rs)*(180/pi)
        lon = atan2(y,x)*180/pi

        ## use the integer, simulation times --  save the UTC/ JD time
        satloc[sat][t] = (time, x, y, z, lat, lon, rs-re)
