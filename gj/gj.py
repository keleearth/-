#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#用于处理数据
class Actuator(object):
    #初始函数,设置所需处理数据的变量
    def __init__(self,fileLocation):
        #要处理的数据所在的文件位置
        self.dataLocation = fileLocation
        #存放从文件中读取出来的数据
        self.data = []
        #----找到数据中共有多少字段
        self.dataSet = set(["DA"])
    #从文件中读取数据并解析
    def readData(self):
        with open(self.dataLocation, 'r',encoding='utf-8') as dataFile:
            # for line in dataFile.readlines():
            #     print(line)
            dataFile.readline()
            dataFile.readline()
            while True:
                data = self.__readOneData(dataFile)
                if(data):
                    self.data.append(data)
                else:
                   break
    #只读取数据文件中的一条数据
    def __readOneData(self, dataFile):
        #每一条记录的数据结构
        dataStruct = {}
        line = dataFile.readline()
        #数据结构每一字段包含的数据
        column=""
        cloumnData=[]
        while line:
            if(line.startswith('\n')):
                break
            else:
                if(line.startswith(' ')):
                    dataStruct[column].append(line[3:].strip('\n'))
                else:
                    column = line[0:2]
                    cloumnData = [line[3:].strip('\n')]
                    dataStruct[column] = cloumnData
                    self.dataSet.add(column)
                # self.data.append(line)
                line = dataFile.readline()
        return dataStruct
        
    #打印data数据，方便查看
    def printData(self):
        for data in self.data:
            print(data)

    #使用pandas对数据进行可视化
    def showData(self):
        dataFrame = pd.DataFrame(self.data)
                


if __name__ == '__main__':
    actuator = Actuator('E:\\project\\python\\data.txt')
    actuator.readData()
    # actuator.printData()
    # print(actuator.dataSet)
    # print(actuator.data[0])
    dictData = actuator.data[0]
    #将data[0]输出到文件
    with open('data\\test.txt', 'w', encoding='utf-8') as testDoc:
        for key in dictData:
            testDoc.write(key + '\t')
            testDoc.write(str(dictData[key]) + "\n")
        testDoc.write(str(actuator.dataSet))

    # print("aa")
