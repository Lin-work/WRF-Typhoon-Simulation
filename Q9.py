from netCDF4 import Dataset
from wrf import getvar, interplevel, latlon_coords, to_np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_paths = [
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-10-02_12:00:00",
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-10-02_18:00:00",
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-10-03_00:00:00",
]

ms_to_knots = 1.94384

levels = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80]
colors = ['#bfbfbf','#a0fffa','#00cdff','#0069ff','#32ff00','#15B01A','#329600','#ffff00','#ffc800', '#ff9600','#ff0000','#c80000','#a00000',
'#96009b','#c800d2','#ff00f5','#ffccff','#FFFFF0']
cmap = ListedColormap(colors)
norm = BoundaryNorm(levels, ncolors=cmap.N,clip=True)



fig, axs = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': ccrs.PlateCarree()})

for i, file_path in enumerate(file_paths):
    ncfile = Dataset(file_path)

    refl = getvar(ncfile, "REFL_10CM", timeidx=0)
    ua = getvar(ncfile, "ua", timeidx=0)
    va = getvar(ncfile, "va", timeidx=0)
    z = getvar(ncfile, "z", timeidx=0)

    refl_2km = interplevel(refl, z, 2000)
    ua_2km = interplevel(ua, z, 2000) * ms_to_knots
    va_2km = interplevel(va, z, 2000) * ms_to_knots

    lats, lons = latlon_coords(refl_2km)

    ax = axs[i]
    ax.set_extent([lons.min(), lons.max(), lats.min(), lats.max()], crs=ccrs.PlateCarree())

    # 繪製雷達回波
    cf = ax.contourf(to_np(lons), to_np(lats), to_np(refl_2km), levels=levels,
                     cmap=cmap,norm=norm, transform=ccrs.PlateCarree())

    # 繪製風羽
    skip = (slice(None, None, 20), slice(None, None, 20))
    ax.quiver(
        to_np(lons)[skip], to_np(lats)[skip],
        to_np(ua_2km)[skip], to_np(va_2km)[skip],
        transform=ccrs.PlateCarree(), scale=1000, width=0.0025
    )

    ax.coastlines('10m')
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.set_title(f"Time: {file_path[-19:]}", fontsize=12)

cbar = fig.colorbar(cf, ax=axs, orientation="horizontal", fraction=0.05, pad=0.1)
cbar.set_label("Reflectivity (dBZ)")

plt.subplots_adjust(wspace=0.1, top=0.88, bottom=0.15)
plt.savefig('Q9-1002-1003.png',dpi=300)
plt.show()

