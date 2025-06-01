import earthpy as ep
import geopandas as gp
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np
from matplotlib.animation import FuncAnimation


#map projection for plot
data = ep.data.get_data('spatial-vector-lidar')
worldBound_path = os.path.join(ep.io.HOME, 'earth-analytics', "data", "spatial-vector-lidar", "global", 
                               "ne_110m_land", "ne_110m_land.shp")
worldBound = gp.read_file(worldBound_path)


class GISMap(tk.Frame):
    def __init__(self, root, master=None):
        tk.Frame.__init__(self,master)
        self.createWidgets(root)

    def createWidgets(self, root):
        # Plot worldBound data using geopandas
        fig, ax = plt.subplots(figsize=(10, 5))
        worldBound.plot(color='darkgrey', 
                        ax=ax)
        # Set the x and y axis labels
        ax.set(xlabel="Longitude (Degrees)",
            ylabel="Latitude (Degrees)",
            title="Global Map - Geographic Coordinate System - WGS84 Datum\n Units: Degrees - Latitude / Longitude")

        # Add the x y graticules
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', 
                    linestyle='dashed')
        ax.xaxis.grid(color='gray', 
                    linestyle='dashed')

        # plt.show()
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=19, column=0, columnspan=3)
        canvas.draw()

        # self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax))
        # self.plotbutton.grid(row=19,column=0)

    def plot(self,canvas,ax):
        c = ['r','b','g']  # plot marker colors
        ax.clear()         # clear axes from previous plot
        for i in range(3):
            theta = np.random.uniform(0,360,10)
            r = np.random.uniform(0,1,10)
            ax.plot(theta,r,linestyle="None",marker='o', color=c[i])
            canvas.draw()

    # def viewingWindows(self, stime, etime, iter, sid, aid):
    #     #stime = start date/time
    #     #etime = end date/time
    #     #iter = iterate by x secs
    #     #sid = satellite id
    #     #aid = address (id)
    #     dur = etime-stime
    #     for t in range(0,dur,iter):
    #         jdate = f(stime, t)


        return

        
# if __name__ == '__main__':
#     def _quit():
#         root.quit()
#         root.destroy()
        
#     root=tk.Tk()
#     root.protocol("WM_DELETE_WINDOW", _quit)
#     app=Application(master=root)
#     root.mainloop()

# # Plot worldBound data using geopandas
# fig, ax = plt.subplots(figsize=(10, 5))
# worldBound.plot(color='darkgrey', 
#                 ax=ax)
# # Set the x and y axis labels
# ax.set(xlabel="Longitude (Degrees)",
#     ylabel="Latitude (Degrees)",
#     title="Global Map - Geographic Coordinate System - WGS84 Datum\n Units: Degrees - Latitude / Longitude")

# # Add the x y graticules
# ax.set_axisbelow(True)
# ax.yaxis.grid(color='gray', 
#             linestyle='dashed')
# ax.xaxis.grid(color='gray', 
#             linestyle='dashed')

# plt.show()
################### data from satellite_watcher ###############################
satellite_position_dict = {0: (44.90519192110561, -65.04187424003952, 412.11188181014404, np.float64(2029.300290744217), np.float64(-4360.165300582248), np.float64(4793.382756371877)), 1: (44.936301414432755, -64.96598115256154, 412.10722801963584, np.float64(2033.9709019384877), np.float64(-4355.111739791644), np.float64(4795.990020006404)), 2: (44.9673548354979, -64.8900012286186, 412.10258574528143, np.float64(2038.6396771256175), np.float64(-4350.053349999246), np.float64(4798.591172829194)), 3: (44.998352062521626, -64.81393443711015, 412.09795499973916, np.float64(2043.306611109881), np.float64(-4344.990137344521), np.float64(4801.186211538262)), 4: (45.02929297356597, -64.73778074793496, 412.0933357956619, np.float64(2047.9716986877886), np.float64(-4339.922107981222), np.float64(4803.775132835251)), 5: (45.06017744669772, -64.66154013154618, 412.0887281456371, np.float64(2052.63493467639), np.float64(-4334.849268048968), np.float64(4806.35793343898)), 6: (45.09100535972756, -64.58521255965753, 412.0841320622676, np.float64(2057.2963138695663), np.float64(-4329.771623718198), np.float64(4808.93461006356)), 7: (45.12177659048542, -64.50879800452519, 412.07954755809897, np.float64(2061.9558310829707), np.float64(-4324.68918114347), np.float64(4811.505159441312)), 8: (45.1524910166101, -64.43229643951175, 412.0749746456622, np.float64(2066.6134811193638), np.float64(-4319.601946499524), np.float64(4814.069578305087)), 9: (45.183148515724426, -64.35570783862651, 412.07041333745747, np.float64(2071.2692587974525), np.float64(-4314.509925951383), np.float64(4816.627863402814)), 10: (45.21374896523781, -64.27903217706312, 412.06586364596296, np.float64(2075.923158918947), np.float64(-4309.413125688577), np.float64(4819.180011480914)), 11: (45.24429224258299, -64.20226943057402, 412.0613255836206, np.float64(2080.575176307522), np.float64(-4304.311551884515), np.float64(4821.726019303962)), 12: (45.27477822496979, -64.12541957613928, 412.056799162855, np.float64(2085.225305767901), np.float64(-4299.205210739244), np.float64(4824.26588363405)), 13: (45.30520678962083, -64.04848259134094, 412.0522843960498, np.float64(2089.87354212471), np.float64(-4294.0941084387805), np.float64(4826.7996012503445)), 14: (45.335577813588024, -63.97145845486808, 412.0477812955878, np.float64(2094.5198801917263), np.float64(-4288.978251187286), np.float64(4829.327168933703)), 15: (45.36589117386436, -63.89434714621842, 412.0432898737963, np.float64(2099.16431479058), np.float64(-4283.857645187597), np.float64(4831.848583475867)), 16: (45.39614674733632, -63.8171486458435, 412.0388101429844, np.float64(2103.8068407420888), np.float64(-4278.732296650042), np.float64(4834.363841675407)), 17: (45.426344410784736, -63.73986293514414, 412.0343421154312, np.float64(2108.447452867013), np.float64(-4273.602211792113), np.float64(4836.872940337704)), 18: (45.45648404091105, -63.66248999642653, 412.0298858034066, np.float64(2113.086145988823), np.float64(-4268.467396834768), np.float64(4839.375876277038)), 19: (45.48656551432594, -63.58502981291255, 412.02544121912706, np.float64(2117.7229149337645), np.float64(-4263.327858003543), np.float64(4841.872646315511)), 20: (45.516588707587026, -63.5074823686769, 412.02100837479065, np.float64(2122.357754534563), np.float64(-4258.183601523275), np.float64(4844.363247286096)), 21: (45.54655349705505, -63.42984764902669, 412.016587282581, np.float64(2126.9906596080673), np.float64(-4253.034633642942), np.float64(4846.847676020598)), 22: (45.576459759161104, -63.352125639791296, 412.01217795463253, np.float64(2131.621624998391), np.float64(-4247.880960589012), np.float64(4849.32592937171)), 23: (45.60630737010604, -63.27431632814765, 412.0077804030625, np.float64(2136.2506455274115), np.float64(-4242.722588618707), np.float64(4851.798004187976)), 24: (45.63609620607893, -63.19641970204083, 412.003394639969, np.float64(2140.8777160299855), np.float64(-4237.559523981864), np.float64(4854.263897331822)), 25: (45.66582614319811, -63.118435750330974, 411.99902067740277, np.float64(2145.5028313456705), np.float64(-4232.391772930726), np.float64(4856.72360567452)), 26: (45.69549705745248, -63.040364462994276, 411.9946585273947, np.float64(2150.125986306566), np.float64(-4227.219341731792), np.float64(4859.177126091248)), 27: (45.72510882477495, -62.962205830907045, 411.9903082019673, np.float64(2154.7471757509456), np.float64(-4222.042236652121), np.float64(4861.624455467075)), 28: (45.754661321019825, -62.883959845930335, 411.98596971308143, np.float64(2159.366394518278), np.float64(-4216.86046396406), np.float64(4864.065590694932)), 29: (45.784154421987814, -62.80562650083892, 411.98164307269417, np.float64(2163.9836374539536), np.float64(-4211.674029940613), np.float64(4866.500528677617)), 30: (45.8135880033561, -62.72720578953566, 411.97732829271627, np.float64(2168.598899396641), np.float64(-4206.482940868678), np.float64(4868.929266321864)), 31: (45.84296194075136, -62.648697706848104, 411.9730253850539, np.float64(2173.212175190913), np.float64(-4201.287203035799), np.float64(4871.351800544308)), 32: (45.872276109738856, -62.570102248573086, 411.9687343615624, np.float64(2177.8234596847833), np.float64(-4196.086822732518), np.float64(4873.7681282704325)), 33: (45.90153038580052, -62.49141941154347, 411.9644552340769, np.float64(2182.432747726126), np.float64(-4190.881806256497), np.float64(4876.178246432657)), 34: (45.93072464432438, -62.41264919367831, 411.9601880144146, np.float64(2187.040034159892), np.float64(-4185.672159915125), np.float64(4878.58215196937)), 35: (45.95985876070035, -62.33379159370344, 411.95593271434154, np.float64(2191.645313845197), np.float64(-4180.457890007522), np.float64(4880.979841832676)), 36: (45.98893261014531, -62.25484661167378, 411.95168934561934, np.float64(2196.2485816245103), np.float64(-4175.239002857598), np.float64(4883.371312973901)), 37: (46.01794606791589, -62.17581424836612, 411.9474579199641, np.float64(2200.849832360033), np.float64(-4170.015504774685), np.float64(4885.756562360974)), 38: (46.046899009134144, -62.096694505791596, 411.9432384490774, np.float64(2205.449060903646), np.float64(-4164.787402086198), np.float64(4888.135586963977)), 39: (46.0757913088942, -62.01748738689685, 411.939030944618, np.float64(2210.046262114914), np.float64(-4159.554701118039), np.float64(4890.508383763783)), 40: (46.10462284220557, -61.93819289574256, 411.93483541822025, np.float64(2214.6414308507983), np.float64(-4154.317408205648), np.float64(4892.874949747284)), 41: (46.133393484041115, -61.8588110373649, 411.9306518814901, np.float64(2219.234561974249), np.float64(-4149.075529684943), np.float64(4895.235281911216)), 42: (46.162103109292296, -61.77934181792484, 411.926480346021, np.float64(2223.825650345615), np.float64(-4143.82907190137), np.float64(4897.58937725837)), 43: (46.19075159281681, -61.699785244571494, 411.9223208233525, np.float64(2228.414690831072), np.float64(-4138.578041200924), np.float64(4899.937232801351)), 44: (46.219338809394024, -61.620141325584505, 411.91817332500705, np.float64(2233.0016782945663), np.float64(-4133.322443938933), np.float64(4902.278845558822)), 45: (46.24786463378415, -61.54041007021341, 411.91403786247974, np.float64(2237.586607607464), np.float64(-4128.062286469267), np.float64(4904.614212560231)), 46: (46.27632894064918, -61.460591488917615, 411.90991444723295, np.float64(2242.1694736348913), np.float64(-4122.797575159539), np.float64(4906.943330839198)), 47: (46.304731604623676, -61.380685593163726, 411.90580309070447, np.float64(2246.7502712479413), np.float64(-4117.528316377804), np.float64(4909.266197439195)), 48: (46.33307250029322, -61.30069239550814, 411.90170380429845, np.float64(2251.3289953190147), np.float64(-4112.2545164972835), np.float64(4911.582809411654)), 49: (46.36135150220742, -61.220611909557775, 411.8976165993872, np.float64(2255.90564072456), np.float64(-4106.976181893767), np.float64(4913.893163816899)), 50: (46.389568484858586, -61.14044415005592, 411.8935414873231, np.float64(2260.480202340216), np.float64(-4101.6933189504925), np.float64(4916.197257722282)), 51: (46.41772332269491, -61.060189132831894, 411.889478479422, np.float64(2265.0526750443455), np.float64(-4096.40593405509), np.float64(4918.4950882031235)), 52: (46.44581589008817, -60.979846874939184, 411.88542758697895, np.float64(2269.623053709949), np.float64(-4091.1140336073836), np.float64(4920.786652339955)), 53: (46.47384606144856, -60.89941739429142, 411.88138882124804, np.float64(2274.1913332263384), np.float64(-4085.8176239962663), np.float64(4923.071947227755)), 54: (46.501813711101626, -60.818900710058905, 411.8773621934606, np.float64(2278.7575084763416), np.float64(-4080.5167116245407), np.float64(4925.3509699657725)), 55: (46.52971871330159, -60.7382968426344, 411.8733477148253, np.float64(2283.3215743387113), np.float64(-4075.2113029065135), np.float64(4927.623717658494)), 56: (46.55756094233439, -60.657605813333774, 411.8693453965079, np.float64(2287.8835257055457), np.float64(-4069.901404248256), np.float64(4929.890187423898)), 57: (46.58534027236195, -60.5768276448699, 411.86535524965166, np.float64(2292.4433574555696), np.float64(-4064.587022078089), np.float64(4932.1503763806395)), 58: (46.61305657765943, -60.495962360657956, 411.8613772853705, np.float64(2297.0010644939066), np.float64(-4059.268162800955), np.float64(4934.404281667242)), 59: (46.640709732291995, -60.41500998578901, 411.8574115147494, np.float64(2301.556641697093), np.float64(-4053.944832861507), np.float64(4936.65190041563))}

## address lla
lata = 37.8506475 
lona = -78.5692074
################### Visualization! #################################
#map projection for plot
data = ep.data.get_data('spatial-vector-lidar')
worldBound_path = os.path.join(ep.io.HOME, 'earth-analytics', "data", "spatial-vector-lidar", "global", 
                               "ne_110m_land", "ne_110m_land.shp")
worldBound = gp.read_file(worldBound_path)

# Plot worldBound data using geopandas
fig, ax = plt.subplots(figsize=(10, 5))
worldBound.plot(color='darkgrey', 
                ax=ax)
# Set the x and y axis labels
ax.set(xlabel="Longitude (Degrees)",
    ylabel="Latitude (Degrees)",
    title="Global Map - Geographic Coordinate System - WGS84 Datum\n Units: Degrees - Latitude / Longitude")

#min and max for each axis
lat_max = max(satellite_position_dict[key][0] for key in satellite_position_dict)
lat_min = min(satellite_position_dict[key][0] for key in satellite_position_dict)
lon_max = max(satellite_position_dict[key][1] for key in satellite_position_dict)
lon_min = min(satellite_position_dict[key][1] for key in satellite_position_dict)

#account for address lla max/min
lat_max = max(lat_max, lata)
lat_min = min(lat_min, lata)
lon_max = max(lon_max, lona)
lon_min = min(lon_min, lona)

ax.set_xlim(lon_min, lon_max) #lon
ax.set_ylim(lat_min,lat_max) #lat
# Add the x y graticules
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', 
            linestyle='dashed')
ax.xaxis.grid(color='gray', 
            linestyle='dashed')

# initializing a line variable

satellite_flight, = plt.plot([], [], 'ro')
address, = plt.plot([lona], [lata], 'bo')

slat = []
slon = []

def init():
    satellite_flight.set_data([],[])
    return satellite_flight,

def update(frame):
    slat.append(satellite_position_dict[frame][0])
    slon.append(satellite_position_dict[frame][1])

    satellite_flight.set_data(slon, slat)
    return satellite_flight, 

ani = FuncAnimation(fig, update, frames=max(list(satellite_position_dict.keys()))+1,
                    init_func=init, blit=True)
plt.show()
