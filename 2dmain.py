import numpy as np
import math
from read_image import readImage, writeImage


proj_1, geotrans_1, data_1 = readImage('F:/CRDC/codeing/filter_vel1.tif')  # 读数据
proj_2, geotrans_2, data_2 = readImage('F:/CRDC/codeing/filter_vel2.tif')  # 读数据
proj_3, geotrans_3, in_1 = readImage('F:/CRDC/codeing/filter_In1.tif')  # 读数据
proj_4, geotrans_4, in_2 = readImage('F:/CRDC/codeing/filter_In2.tif')  # 读数据

data_1 = np.array(data_1)
data_2 = np.array(data_2)
in_1 = np.array(in_1)
in_2 = np.array(in_2)
bands, rows, cols = data_1.shape  #band1:LOS沉降速率 band2：Lon band3:Lat band4:入射角 band5:高程？待定
ASC_AN = math.pi * -1.269695612e+01/180
DSC_AN = math.pi * -1.6734001859e+02/180

LOS = np.empty([2,rows,cols]) #升轨、降轨得到的LOS沉降速率联合
ANG = np.empty([2,rows,cols]) #升轨、降轨得到的各点入射角联合
for i in range (rows):
    for j in range (cols):
        if(data_1[0,i,j]!=0 and data_2[0,i,j]!=0):
            LOS[0, i, j] = data_1[0, i, j]
            LOS[1, i, j] = data_2[0, i, j]
            ANG[0, i, j] = in_1[0, i, j]
            ANG[1, i, j] = in_2[0, i, j]
        else:
            LOS[:, i, j] = [0,0]
            ANG[:, i, j] = [0,0]
a = np.empty([2,2])
b = np.empty([2,rows,cols])
# np.linalg.inv(a) 矩阵求逆
for i in range(rows):
    for j in range(cols):
        a = [[math.cos(math.radians(ANG[0,i,j])), -1*math.cos(ASC_AN)*math.sin(math.radians(ANG[0,i,j]))],
             [math.cos(math.radians(ANG[1, i, j])), -1 * math.cos(DSC_AN) * math.sin(math.radians(ANG[1, i, j]))]]
        a = np.array(a)
        if(LOS[0,i,j]==0 or LOS[1,i,j]==0):
            b[:,i,j] = [0,0]
        else:
            m = np.linalg.inv(a)
            n = LOS[:,i,j].reshape(-1,1)
            k = np.dot(m,n)
            b[:, i, j] = np.squeeze(k)


writeImage(b, path='ZY3.tif', geotrans=geotrans_1, proj=proj_1)



