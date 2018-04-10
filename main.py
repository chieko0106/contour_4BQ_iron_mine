# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
from readGDN import F
from XYZ_3Dmodel import File


path = 'F:\\3-柏泉铁矿\\柏泉铁矿强度折减有限元计算\\pline\\'
count = 0
data = {'X':[],'Y':[],'Z':[]}
for z0 in range(550,720,5):
    file = str(z0)+'.txt'
    In = F(path,file,z0)
    In.Read()
    In.maskRead([40384500.0000, 40385600.0000], [4541588.0000, 4542000.0000], [-1, 10000])
    for i in range(len(In.data['X'])):
        data['X'].append(In.data['X'][i])
        data['Y'].append(In.data['Y'][i])
        data['Z'].append(In.data['Z'][i])
        count = count + 1

path = 'F:\\3-柏泉铁矿\\柏泉铁矿强度折减有限元计算\\'
file = 'points.txt'

In_po = File(path,file)
In_po.Read()
In_po.maskRead([40384500.0000,40385600.0000],[4541588.0000,4542000.0000],[-1,10000])

for i in range(len(In_po.data['X'])):
    data['X'].append(In_po.data['X'][i])
    data['Y'].append(In_po.data['Y'][i])
    data['Z'].append(In_po.data['Z'][i])
    count = count + 1

fig = plt.figure()
ax0 =  fig.add_subplot(311)
ax0.scatter(data['X'],data['Y'],c = data['Z'])
ax0.grid(True)

# 根据输入的点，形成高程三角网
points = np.zeros((count, 2))
points[:, 0] = data['X']
points[:, 1] = data['Y']
tri = Delaunay(points)


# 画三角网
ax1 =  fig.add_subplot(312)
ax1.tricontourf(data['X'], data['Y'], tri.simplices.copy(),data['Z'] )
#matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
#CS = plt.tricontour(In.data['X'], In.data['Y'], tri.simplices.copy(),In.data['Z'], 8, colors='black', linewidth=.1)
#plt.clabel(CS, inline=1, fontsize=12,fmt = '%1.0f',inline_spacing=.5)

# 由于三角网的结果明显不好，用插值的方法再画一次
coords = data
x = coords['X']
y = coords['Y']
z = np.array(coords['Z'])
triang = mtri.Triangulation(x, y)
# Interpolate to regularly-spaced quad grid.
xi, yi = np.meshgrid(np.linspace(min(x), max(x),1000), np.linspace(min(y), max(y), 1000))
interp_z = mtri.LinearTriInterpolator(triang, z)
# interp_z = mtri.CubicTriInterpolator(triang, z,kind='geom')
zi= interp_z(xi, yi)
ax2 = fig.add_subplot(313)
ax2.contourf(xi,yi,zi)

plt.show()

print('end')