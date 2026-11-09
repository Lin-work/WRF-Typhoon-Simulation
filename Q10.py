from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 檔案路徑
file_paths = [f"/work/u9792397/wrf/WRFV4.5.2/run/wrfout_d02_2024-{D}_00:00:00" for D in ['09-30', '10-01', '10-02', '10-03']]

typhoon_path = []
labels = []

for file_path in file_paths:
    ncfile = Dataset(file_path)

    # 取出850hPa的風場
    vort = getvar(ncfile, "avo")[16]
    va = getvar(ncfile, "va", units="m s-1")
    pressure = getvar(ncfile, "pres", units="hPa")
    print(pressure[:,0,0])
    print(len(va))
    print(pressure[16,0,0])
    #vort = vorticity(ua, va)
    vort_np = to_np(vort)
    lats, lons = latlon_coords(vort)
    lat, lon = latlon_coords(va)
    lat_np = to_np(lats)
    lon_np = to_np(lons)

    # 找到最大渦度位置
    max_idx = np.unravel_index(np.argmax(vort_np), vort_np.shape)
    center_lat = lat_np[max_idx]
    center_lon = lon_np[max_idx]
    typhoon_path.append((center_lon, center_lat))

    # 擷取日期標籤
    date_str = file_path.split("_")[2][5:].replace("-", "/")
    labels.append(date_str)

lons, lats = zip(*typhoon_path)

plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.set_title("Typhoon Track based on Max Vorticity (538 hPa)", fontsize=14)
ax.plot(lons, lats, marker='o', color='red', linestyle='-', label='Typhoon Path')

for lon, lat, label in zip(lons, lats, labels):
    ax.text(lon + 0.2, lat + 0.2, label, fontsize=10, transform=ccrs.PlateCarree())

ax.gridlines(draw_labels=True)
plt.legend()
plt.savefig('Q10-v2.png',dpi=300)
plt.show()
