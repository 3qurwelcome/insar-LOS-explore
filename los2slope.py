import xlrd
import numpy as np
import math
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# LOS形变 分解
# 适用于滑坡，分解为坡向形变
# 参考文献
# Davide Notti, Gerardo Herrera, Silvia Bianchini, Claudia Meisina, Juan Carlos
# García-Davalillo & Francesco Zucca (2014) A methodology for improving landslide PSI data analysis,
# International Journal of Remote Sensing, 35:6, 2186-2214
# A methodology for improving landslide PSI data analysis
# 先前版本没有矢量处理，仅为对Excel操作，后加入矢量处理以达到可视化目的。
# 路志远 2020.8.6
resArray=[]  # 先声明一个空list
# data = xlrd.open_workbook('F:/CRDC/luzy/TableToExcel.xls')  # 可以通过shape file to excel 得到？
data = xlrd.open_workbook('Save_Excel.xls')
sf = gpd.read_file("test.shp")
# sf = gpd.read_file("F:/CRDC/luzy/dsc_2.shp")
table = data.sheet_by_index(0)  # 按索引获取工作表，0就是工作表1
for i in range(table.nrows):  # table.nrows表示总行数
    line=table.row_values(i)  # 读取每行数据，保存在line里面，line是list
    resArray.append(line)  # 将line加入到resArray中，resArray是二维list
resArray=np.array(resArray)[1:,].astype(float)  # 将resArray从二维list变成数组
print(resArray)

# 分解计算
row, col = resArray.shape
Vslope = np.empty([row,1])
for i in range(row):
    LOS = resArray[i, 1]
    A = math.pi * resArray[i, 2]/180
    S = math.pi * resArray[i, 3]/180
    alpha = math.pi * resArray[i, 5]/180
    gamma = math.pi * resArray[i, 4]/180
    H = math.cos(alpha)
    E = -1 * math.sin(alpha) * math.sin(gamma)
    N = -1 * math.sin(alpha) * math.cos(gamma)
    C = N * (math.cos(S) * math.cos(A) * -1) - E * (math.sin(A) * math.cos(S)) + H * math.sin(S)
    if(C>=-0.3 and C<0):
        C=-0.3
    elif(C>0 and C<=0.3):
        C=0.3
    Vslope[i,:] = LOS/C

# 连接到矢量
data_df = pd.DataFrame(Vslope,columns=['VSLOPE'])
sf = sf.merge(data_df,left_index=True,right_index=True,how='outer')

# 可视化显示
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs = sf['X']
ys = sf['Y']
zs = sf['Z']
c = sf['VSLOPE']
sc = ax.scatter(xs, ys, zs, s=0.1, c=c, cmap='hsv')
ax.set_ylabel('N', loc='top')
ax.set_xlabel('E', loc='left')
cbar = fig.colorbar(sc, shrink=0.5, aspect=5)
cbar.set_label("Velocity", loc='top')
plt.show()

# 保存shapefile
sf.to_file("dsc_slopeV.shp")

# writer = pd.ExcelWriter('Save_Excel_2.xls')
# data_df.to_excel(writer, 'page_1', float_format='%.9f') # float_format 控制精度
# writer.save()
