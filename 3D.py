# -*- coding: UTF-8 -*-
'''
根据散点的数据生成三维面，包括多段线和散点
散点的格式：
X Y Z
0.0 0.0 0.0
...
多段线的格式是gdn输出的格式，多段线命名为 （高程值）.txt
'''
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as mtri
from scipy.spatial import Delaunay
from readGDN import F
from XYZ_3Dmodel import File
from mpl_toolkits.mplot3d import Axes3D

path = 'F:\\3-柏泉铁矿\\柏泉铁矿强度折减有限元计算\\pline\\'
count = 0
data = {'X': [], 'Y': [], 'Z': []}
for z0 in range(550, 720, 5):
    file = str(z0) + '.txt'
    In = F(path, file, z0)
    In.Read()
    In.maskRead([40384500.0000, 40385600.0000], [4541588.0000, 4542000.0000], [-1,1000])
    for i in range(len(In.data['X'])):
        data['X'].append(In.data['X'][i])
        data['Y'].append(In.data['Y'][i])
        data['Z'].append(In.data['Z'][i])
        count = count + 1

path = 'F:\\3-柏泉铁矿\\柏泉铁矿强度折减有限元计算\\'
file = 'points.txt'

In_po = File(path, file)
In_po.Read()
In_po.maskRead([40384500.0000, 40385430.0000], [4541689.0000, 4542000.0000], [-1, 665])

for i in range(len(In_po.data['X'])):
    data['X'].append(In_po.data['X'][i])
    data['Y'].append(In_po.data['Y'][i])
    data['Z'].append(In_po.data['Z'][i])
    count = count + 1





fig = plt.figure()
ax0 = fig.add_subplot(111, projection='3d')
# 生成结构化网格数据
coords = data
x = coords['X']
y = coords['Y']
z = np.array(coords['Z'])
triang = mtri.Triangulation(x, y)
# Interpolate to regularly-spaced quad grid.
xi, yi = np.meshgrid(np.linspace(min(x), max(x), 100), np.linspace(min(y), max(y), 100))
interp_z = mtri.LinearTriInterpolator(triang, z)
# interp_z = mtri.CubicTriInterpolator(triang, z,kind='geom')
zi = interp_z(xi, yi)

filename = path+'write_tec.dat'
with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("TITLE\t=\t\"terrain\"\n")
    f.write("VARIABLES\t= \"X\",\"Y\",\"Z\"\n")
    f.write("ZONE\tT=\"P1\",\tN=")
    f.write(str(count))
    f.write(",\tE=\t")
    f.write(str(len(triang.triangles)))
    f.write(",DATAPACKING=POINT, ZONETYPE=FETRIANGLE\n")
    for i in range(count):
        f.write(str(x[i])+"\t")
        f.write(str(y[i])+"\t")
        f.write(str(z[i]))
        f.write("\n")
    for item in triang.triangles:
        f.write(str(item[0]+1) + "\t")
        f.write(str(item[1]+1) + "\t")
        f.write(str(item[2]+1) + "\t")
        f.write("\n")



from matplotlib import cm
from matplotlib.colors import LightSource

ls = LightSource(270, 45)
rgb = ls.shade(zi, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax0.plot_surface(xi, yi, zi, rstride=1, cstride=1, facecolors=rgb,
                        linewidth=0, antialiased=False, shade=False)
plt.show()
print('end')
