# -*- coding: UTF-8 -*-
'''
对于简单边坡，生成结构化网格拓扑的程序
因为是针对边坡，这里预设不存在90度坡，因此用在其它地方的时候可能会有问题
输入的x，y必须是按照从坡顶到坡脚的顺序，并且对应排列
'''
import matplotlib.pyplot as plt
import numpy as np

def Read(path,file):
    __f = open(path+file)
    data = {'X': [], 'Y': []}
    count = 0
    for line in __f:
        line = line[0:-1]
        line = line.split('\t')
        data['X'].append(float(line[0]))
        data['Y'].append(float(line[1]))
        count += 1
    return data, count

path = 'F:\\3-柏泉铁矿\\柏泉铁矿强度折减有限元计算\\'
file = 'slice4.txt'
data,count = Read(path,file)

extra_depth = 100 # 在这里定义模型下面要加深多少
extra_left = 50 # 定义左边增加多少，正值
extra_right = 50 #定义右边增加多少，正值
min_Element = 15 # 定义单元的大概大小
if extra_right != 0:
    imax = data['X'].index(max(data['X']))
    data['X'].append(data['X'][imax]+extra_right)
    data['Y'].append(data['Y'][imax])
if extra_left != 0:
    imin = data['X'].index(min(data['X']))
    data['X'].insert(0,(data['X'][imin] - extra_left))
    data['Y'].insert(0,(data['Y'][imin]))
X = data['X']
Y = data['Y']
coordYs = []


i = 0
while i < len(X):
    if i !=0:
        while abs(X[i] - X[i-1]) > min_Element:
            X.insert(i, (X[i] + X[i-1])/2)
            Y.insert(i, (Y[i] + Y[i - 1]) / 2)
    i += 1

for i in Y:
    if i not in coordYs:
        coordYs.append(i)
coordYs.append(min(coordYs)-extra_depth)

i = 0
while i < len(coordYs):
    if i !=0:
        while abs(coordYs[i] - coordYs[i-1]) > min_Element:
            coordYs.insert(i, (coordYs[i] + coordYs[i-1])/2)
    i += 1


baseline = min(Y) - extra_depth
NumcoordY = int((max(Y)-baseline)/(max(X)-min(X))*len(X))
coordYs = np.linspace(baseline, max(Y),NumcoordY)
node = {}
for i in range(len(X)):
    xx = X[i]
    temp = [coordYs[0]]
    if i == 0:
        height0 = Y[i] - baseline
        node[str(min(X))] = coordYs
        continue
    height = Y[i] - baseline
    for j in range(len(coordYs)-1):
        dh = height/height0*(coordYs[j+1]-coordYs[j])
        temp.append(temp[-1]+dh)
    node[str(xx)] = temp




fig = plt.figure()
ax0 = fig.add_subplot(111)
for key in node.keys():
    yi = node[key]
    xi = [float(key) for i in range(len(yi))]
    ax0.scatter(xi,yi)
plt.show()

#写tecplot文件
filename = path+'mesh.dat'
NumX = len(node.keys())
NNode = NumX*len(coordYs)
NEle = (NumX-1)*(len(coordYs)-1)
with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write("TITLE\t=\t\"terrain\"\n")
    f.write("VARIABLES\t= \"X\",\"Y\",\"Z\"\n")
    f.write("ZONE\tT=\"mesh\",\tN=")
    f.write(str(NNode*2))
    f.write(",\tE=\t")
    f.write(str(NEle))
    f.write(",F=FEPOINT, ET=BRICK\n")
    D = 0
    while D <2:
        for i in range(len(coordYs)):
            for key in node.keys():
                f.write(str(D*min_Element)+"\t"+key+"\t"+str(node[key][i])+"\n")
        D += 1
    for i in range(NNode-NumX-1):
        if (i+1)%NumX != 0:
            f.write(str(i+1)+"\t"+str(i+2)+"\t")
            f.write(str(i + 2 + NumX) + "\t" + str(i + 1 + NumX) + "\t")
            f.write(str(i + 1 + NNode) + "\t" + str(i + 2+ NNode) + "\t")
            f.write(str(i + 2 + NumX + NNode) + "\t" + str(i + 1 + NumX + NNode) + "\n")


print("end")