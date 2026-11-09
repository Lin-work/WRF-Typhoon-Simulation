from netCDF4 import Dataset
from wrf import getvar, to_np, latlon_coords
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# WRF 檔案列表
file_paths = [
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d01_2024-09-30_00:00:00",
    "/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-09-30_00:00:00",
]

# 色階
levels = np.linspace(0, 3000, 15)

# 繪圖函數
def plot_temp(lon, lat, data, domain, title):
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    print(lon.min(), lon.max(), lat.min(), lat.max())
    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())

    contour = ax.contourf(lon, lat, data, levels=levels, cmap="terrain",extend="max", transform=ccrs.PlateCarree())
    plt.colorbar(contour, orientation="vertical", label="Height (m)")

    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    ax.set_title(f"{title}", fontsize=14)

    gl = ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.1)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}
    plt.savefig(f'Q6-{domain}.png',dpi=300)
    #plt.show()

# 主程式
for i, file_path in enumerate(file_paths):
    ncfile = Dataset(file_path)
    print(ncfile)
    # 使用 wrf-python 取得變數
    height = getvar(ncfile, "ter", timeidx=0)
    lats, lons = latlon_coords(height)

    # 轉成 numpy array
    height_np = to_np(height)
    lat_np = to_np(lats)
    lon_np = to_np(lons)

    plot_temp(
        lon_np, lat_np, height_np, domain=f"{file_path[40:43]}",
        title=f"Terrain and Coastline {file_path[40:43]} "
    )
