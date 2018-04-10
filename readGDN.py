# -*- coding: UTF-8 -*-
class F:
    data = {}
    count = 0
    def __init__(self,path,file,z0 = 0):
        self.__path = path
        self.__file = file
        self.__z0 = z0

    def Read(self):
        __f = open(self.__path + self.__file)
        F.data = {'X':[],'Y':[],'Z':[]}
        for line in __f:
            line = line[0:-1]
            line = line.split('\t')
            if len(line) < 2:# 跳过空行
                continue
            if float(line[0]) < 1000: # 跳过标识行
                continue
            F.data['X'].append(float(line[0]))
            F.data['Y'].append(float(line[1]))
            F.data['Z'].append(self.__z0)
            F.count += 1
    def maskRead(self,X,Y,Z):
        xx = F.data['X']
        yy = F.data['Y']
        zz = F.data['Z']
        x = []
        y = []
        z = []
        F.count = 0
        for i in range(len(xx)):
            if xx[i] > X[0] and xx[i] < X[1] and yy[i] > Y[0] and yy[i] < Y[1]and zz [i] > Z[0] and zz[i] < Z[1]:
                x.append(xx[i])
                y.append(yy[i])
                z.append(zz[i])
                F.count += 1
        F.data['X'] = x
        F.data['Y'] = y
        F.data['Z'] = z
