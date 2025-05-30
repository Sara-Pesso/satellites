import earthpy as ep
import geopandas as gp
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk  
import numpy as np

#map projection for plot
data = ep.data.get_data('spatial-vector-lidar')
worldBound_path = os.path.join(ep.io.HOME, 'earth-analytics', "data", "spatial-vector-lidar", "global", 
                               "ne_110m_land", "ne_110m_land.shp")
worldBound = gp.read_file(worldBound_path)


class Application(tk.Frame):
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
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()

        self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax))
        self.plotbutton.grid(row=0,column=0)

    def plot(self,canvas,ax):
        c = ['r','b','g']  # plot marker colors
        ax.clear()         # clear axes from previous plot
        for i in range(3):
            theta = np.random.uniform(0,360,10)
            r = np.random.uniform(0,1,10)
            ax.plot(theta,r,linestyle="None",marker='o', color=c[i])
            canvas.draw()
    
        
# if __name__ == '__main__':
#     def _quit():
#         root.quit()
#         root.destroy()
        
#     root=tk.Tk()
#     root.protocol("WM_DELETE_WINDOW", _quit)
#     app=Application(master=root)
#     root.mainloop()