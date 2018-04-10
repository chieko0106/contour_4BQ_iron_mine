# -*- coding: UTF-8 -*-
class File:
    data = {}
    control = []
    count = 0
    mod = {'IF':False,'X0':0,'Y0':0}
    def __init__(self,path,file):
        self.__path = path
        self.__file = file
    def Read(self):
        __f = open(self.__path+self.__file)
        File.data = {}
        for line in __f:
            if line[0].isalpha():
                line = line[0:-1]
                line = line.split('\t')
                File.control = line
            else:
                line = line[0:-1]
                line = line.split('\t')
                for i in range(len(File.control)):
                    if File.control[i] not in File.data.keys():
                        File.data[File.control[i]] = []
                    File.data[File.control[i]].append(float(line[i]))
                File.count += 1
        __f.close()
    def maskRead(self,X,Y,Z):
        xx = File.data['X']
        yy = File.data['Y']
        zz = File.data['Z']
        x = []
        y = []
        z = []
        File.count = 0
        for i in range(len(xx)):
            if xx[i] > X[0] and xx[i] < X[1] and yy[i] > Y[0] and yy[i] < Y[1]and zz [i] > Z[0] and zz[i] < Z[1]:
                x.append(xx[i])
                y.append(yy[i])
                z.append(zz[i])
                File.count += 1
        File.data['X'] = x
        File.data['Y'] = y
        File.data['Z'] = z
