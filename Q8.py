import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
import numpy as np
from wrf import getvar, interplevel, to_np, get_cartopy, latlon_coords

# 讀取兩個時間點的 wrfout 檔 (第0小時、第24小時)
ncfile_0 = Dataset("/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-10-02_00:00:00")
ncfile_24 = Dataset("/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-10-03_00:00:00")

# 抓取 RAINC 和 RAINNC 變數
rainc_0 = getvar(ncfile_0, "RAINC",timeidx=0)
rainnc_0 = getvar(ncfile_0, "RAINNC", timeidx=0)
rainc_24 = getvar(ncfile_24, "RAINC", timeidx=0)
rainnc_24 = getvar(ncfile_24, "RAINNC", timeidx=0)
tsk = getvar(ncfile_24, "TSK", timeidx=0)
# 計算累積雨量
rain_24hr = (rainc_24 + rainnc_24) - (rainc_0 + rainnc_0)
lats, lons = latlon_coords(rain_24hr)
print(lats,lons)

levels = [0,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300]
colors = ['#bfbfbf','#a0fffa','#00cdff','#0096ff','#0069ff','#329600','#32ff00','#ffff00','#ffc800', '#ff9600','#ff0000','#c80000','#a00000',
'#96009b','#c800d2','#ff00f5','#ffccff']
cmap = ListedColormap(colors)
norm = BoundaryNorm(levels, ncolors=cmap.N,clip=True)

def plot_temp(lon, lat, data, title, domain):
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    #print(lon.min(), lon.max(), lat.min(), lat.max())
    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())

    contour = ax.contourf(lon, lat, data,levels=levels,cmap=cmap,norm=norm,extend='max', transform=ccrs.PlateCarree())
    plt.colorbar(contour, orientation="vertical", label="Rainfall (mm)")

    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    ax.set_title(f"{title}", fontsize=14)

    gl = ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.1)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}
    plt.savefig(f'Q8-1002-1003.png',dpi=300)
    plt.show()


# 轉成 numpy array
lat_np = to_np(lats)
lon_np = to_np(lons)
rain_np = to_np(rain_24hr)
plot_temp(
   lon_np, lat_np, rain_24hr,
   title=f"WRF D01 24hr Accumulated Rainfall \n 10/02 00:00 ~ 10/03 00:00",
   domain=1,
)