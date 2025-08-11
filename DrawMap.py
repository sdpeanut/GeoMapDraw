import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import cartopy.crs as ccrs

# 读取shp文件
shapefile_path = 'map/world-administrative-boundaries.shp'  # 替换为你shp文件的路径
gdf = gpd.read_file(shapefile_path)

# 读取Excel文件，假设Excel文件名为 'data.xlsx'
excel_path = 'data.xlsx'  # 替换为你的 Excel 文件路径
df = pd.read_excel(excel_path)

# 查看Excel文件内容
print(df.head())  # 查看前几行，确保数据格式正确

# 创建地理数据（点），使用第三列和第四列作为经纬度
geometry = [Point(xy) for xy in zip(df['经度'], df['纬度'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)

# 设置自定义投影，将中心经度设为东经 155 度
projection = ccrs.PlateCarree(central_longitude=155)

# 获取唯一类型
unique_types = df['ALL'].unique()

# 创建3个纵向排列的子图，figsize 可以根据需要调整
fig, axes = plt.subplots(nrows=len(unique_types), ncols=1, figsize=(10, 8 * len(unique_types)),
                         subplot_kw={'projection': projection})

# 定义不同类型的颜色和形状
base_colors = ['red', 'red', 'orange', 'brown']
base_markers = ['o', 'o', '^', 'D', '*', 'v']
markers = {}

# 为每个类型分配颜色和形状
for idx, t in enumerate(unique_types):
    markers[t] = {'color': base_colors[idx % len(base_colors)],
                  'marker': base_markers[idx % len(base_markers)]}

# 绘制每个类型对应的地图
for idx, t in enumerate(unique_types):
    ax = axes[idx]  # 当前的子图
    gdf.plot(ax=ax, facecolor='#377eb8', edgecolor='white', linewidth=0.5, transform=ccrs.PlateCarree())

    # 根据类型绘制每个点
    subset = geo_df[geo_df['ALL'] == t]
    ax.scatter(subset.geometry.x, subset.geometry.y,
               color=markers[t]['color'],
               marker=markers[t]['marker'],
               label=t,
               s=30,  # 标记的大小
               edgecolor='black',
               transform=ccrs.PlateCarree())  # 保持投影的一致性

    # 添加图例并放置在下方中央位置
    ax.legend(title=f'类型: {t}', loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)

    # 设置轴的背景颜色为白色
    ax.set_facecolor('white')

    # 去掉坐标轴和边框
    ax.axis('off')

# 自动适应不同屏幕比例时的布局间距（防止图例被裁切）：
plt.tight_layout()

# 保存图形为PDF
plt.savefig('SV.pdf', format='pdf', bbox_inches='tight')

# 显示地图
plt.show()
