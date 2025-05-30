from math import *
import numpy as np
re = 6378 # km; radius of Earth (assuming spherical Earth)

def azel(x1,y1,z1,x2,y2,z2):
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

    return az, el

def LOS_geometry(lat1,lon1,alt1, lat2,lon2,alt2):
    
    lat1, lon1, lat2, lon2 = lat1*pi/180, lon1*pi/180, lat2*pi/180, lon2*pi/180 ##convert deg to rad

    cos_lambda_01 = re/(re+alt1)
    cos_lambda_02 = re/(re+alt2)
    lambda_01 = acos(cos_lambda_01) #radians
    lambda_02 = acos(cos_lambda_02) #radians
    
    cos_lambda = sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(abs(lon1-lon2))
    lambda_ = acos(cos_lambda) #radians

    ##lambda check
    #lla-to-ecef
    xa = (re+alt1)*cos(lat1)*cos(lon1)
    ya = (re+alt1)*cos(lat1)*sin(lon1)
    za = (re+alt1)*sin(lat1)

    xs = (re+alt2)*cos(lat2)*cos(lon2)
    ys = (re+alt2)*cos(lat2)*sin(lon2)
    zs = (re+alt2)*sin(lat2)

    norma = sqrt(xa**2+ya**2+za**2)
    norms = sqrt(xs**2+ys**2+zs**2)
    cos_l = (xa*xs + ya*ys + za*zs)/(norma*norms)
    l_check = acos(cos_l) #radians
    print("check lambda:", lambda_, l_check)

    if lambda_ > (lambda_01+lambda_02):
        LOS = False
    else:
        LOS = True
    
    if LOS == True:
        D = sqrt((za-zs)**2+(ya-ys)**2+(xa-xs)**2)

        # tan_theta1 = ((re+alt2)*sin(lambda_))/((re+alt1)-(re+alt2)*cos(lambda_))
        # tan_theta2 = ((re+alt1)*sin(lambda_))/((re+alt2)-(re+alt1)*cos(lambda_))
        # theta1 = atan2((re+alt2)*sin(lambda_), (re+alt1)-(re+alt2)*cos(lambda_))
        # theta2 = atan2((re+alt1)*sin(lambda_), (re+alt2)-(re+alt1)*cos(lambda_))

        # using the law of sines
        sin_theta1 = (re+alt2)*sin(lambda_)/D
        sin_theta2 = (re+alt1)*sin(lambda_)/D

        #EL --"viewing angle"
        theta1 = pi/2 - asin(sin_theta1)
        theta2 = pi/2 - asin(sin_theta2)
        ## this also requires some logic...
        K1 = (re+alt2)*cos(lambda_)
        if (re+alt1) < K1:
            theta1 = abs(theta1)
        elif (re+alt1) > K1:
            theta1 = -abs(theta1)
        elif (re+alt1) == K1:
            theta1 = 0

        K2 = (re+alt1)*cos(lambda_)
        if (re+alt2) < K2:
            theta2 = abs(theta2)
        elif (re+alt2) > K2:
            theta2 = -abs(theta2)
        elif (re+alt2) == K2:
            theta2 = 0


        range_ = (re+alt2)*sin(lambda_)/sin(theta1)
        # print("check range:", D, range_)
        
        #az -- viewing angle
        cos_phi1 = (sin(lat2) - cos(lambda_)*sin(lat1))/(sin(lambda_)*cos(lat1))
        cos_phi2 = (sin(lat1) - cos(lambda_)*sin(lat2))/(sin(lambda_)*cos(lat2))
        phi1 = acos(cos_phi1)
        phi2 = acos(cos_phi2)

        ## this doesnt account for the sign! need some logic like this...

        if abs(lon1) == 180 and lon2 >= 0:
            lon1 = 180
        elif abs(lon1) == 180 and lon2 < 0:
            lon1 = -180
        elif abs(lon2) == 180 and lon1 >= 0:
            lon2 = 180
        elif abs(lon2) ==180 and lon1 < 0:
            lon2 = -180
        
        if lon1 < lon2: #if (1) is east of (2)
            phi1 = abs(phi1)
            phi2 = -abs(phi2)
        else: #if (1) is west of (2)
            phi1 = -abs(phi1)
            phi2 = abs(phi2)


        print("az el (phi/theta):", phi1*180/pi, theta1*180/pi)

        az, el = azel(xa,ya,za,xs,ys,zs) #output in radians
        print("azel checker:",az*180/pi,el*180/pi)

        ##
        az2, el2 = azel(xs,ys,zs,xa,ya,za)
        print("az el (phi/theta)2:", phi2*180/pi, theta2*180/pi)
        print("azel checker2:",az2*180/pi,el2*180/pi)
        print("check az sum:", az*180/pi + az2*180/pi)

        return (LOS, lambda_01, lambda_02, lambda_, phi1, phi2, theta1, theta2, D, az, el) ## outputs in radians

    else:
        return (LOS, nan, nan, nan, nan, nan, nan, nan, nan, nan,nan)