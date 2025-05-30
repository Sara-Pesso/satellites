from math import *
# from geometry import *
import numpy as np
re = 6378 # km; radius of Earth (assuming spherical Earth)

az = 50*pi/180
el = 35*pi/180

dx = cos(az)*cos(el)
dy = sin(az)*cos(el)
dz = sin(el)

##

az = atan2(dy,dx)*180/pi
el = asin(dz/sqrt(dx**2+dy**2+dz**2))*180/pi
# el2 = asin(dz)

# print(az,el)

x1,y1,z1 = 1285410, -4797210, 3994830
x2,y2,z2 = 1202990, -4824940, 3999870

def azel(x1,y1,z1,x2,y2,z2):
    dx = x2-x1
    dy = y2-y1
    dz = z2-z1
    cos_el = (x1*dx + y1*dy + z1*dz)/(sqrt((x1**2+y1**2+z1**2)*(dx**2+dy**2+dz**2)))
    el = acos(cos_el)

    cos_az = (-z1*x1*dx - z1*y1*dy + (x1**2+y1**2)*dz)/(sqrt((x1**2+y1**2)*(x1**2+y1**2+z1**2)*(dx**2+dy**2+dz**2)))
    sin_az = (-y1*dx+x1*dy)/(sqrt((x1**2+y1**2)*(dx**2+dy**2+dz**2)))
    az = atan2(sin_az, cos_az)
    return az*180/pi, 90-el*180/pi

az,el = azel(x1,y1,z1,x2,y2,z2)
print(az,el)
## correct as far as the gis stack exchange is concerned

def azel2(x1,y1,z1,x2,y2,z2):
    # https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates
    r = sqrt(x1**2+y1**2+z1**2)
    lat = (pi/2) - acos(z1/r)
    lon = atan2(y1,x1)

    v1 = np.array([x1,y1,z1])
    v2 = np.array([x2,y2,z2])
    LOS_hat = (v2-v1)/sqrt((v2-v1).dot(v2-v1))
    
    e_hat = np.array([-sin(lon), cos(lon), 0])
    n_hat = np.array([-cos(lon)*sin(lat), -sin(lon)*sin(lat), cos(lat)])
    u_hat = np.array([cos(lon)*cos(lat), sin(lon)*cos(lat), sin(lat)])

    el = asin(LOS_hat.dot(u_hat))
    az = atan2(LOS_hat.dot(e_hat), LOS_hat.dot(n_hat))

    return az*180/pi, el*180/pi

az,el = azel2(x1,y1,z1,x2,y2,z2)
print(az,el)