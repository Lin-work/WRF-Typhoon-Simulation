
from netCDF4 import Dataset
from wrf import getvar, to_np, latlon_coords
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# WRF 檔案列表
file_paths = [
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-09-30_00:00:00",
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-09-30_01:00:00",
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-09-30_02:00:00",
]

# 色階
levels = np.linspace(280, 310, 13)
# 建立整體圖框與子圖 (一列三圖)
fig, axs = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': ccrs.PlateCarree()})
domain = 1
for i, file_path in enumerate(file_paths):
    ncfile = Dataset(file_path)

    # 取得變數
    tsk = getvar(ncfile, "TSK", timeidx=0)
    lats, lons = latlon_coords(tsk)

    # 轉 numpy
    temp_np = to_np(tsk)
    lat_np = to_np(lats)
    lon_np = to_np(lons)

    ax = axs[i]
    ax.set_extent([lon_np.min(), lon_np.max(), lat_np.min(), lat_np.max()], crs=ccrs.PlateCarree())

    contour = ax.contourf(lon_np, lat_np, temp_np, levels=levels, cmap="coolwarm",extend="both", transform=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    ax.set_title(f"Surface Temperature {file_path[-19:]} (t+{i}h) \n D02", fontsize=10)
    gl = ax.gridlines(draw_labels=(i==i),color='gray', linestyle='--', linewidth=0.2)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}
    plt.tight_layout()

# 加入 colorbar（共用）
cbar = fig.colorbar(contour,ax=axs,location='right',label="Temperature (K)")
plt.savefig('Q7-d02.png',dpi=300)
#plt.show()
