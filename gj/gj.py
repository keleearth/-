#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#用于处理数据
class Actuator(object):

    fieldMapping = {'RI':'ResearcherID 号',
                    'PD':'出版日期',
                    'PY':'出版年',
                    'TI':'文献标题',
                    'CL':'会议地点',
                    # 'EF':'文件结束',
                    # 'FN':'文件名',
                    'DA':'生成此报告日期',
                    'SI':'特刊',
                    'DT':'文献类型',
                    'BP':'开始页',
                    # 'ER':'记录结束',
                    'OA':'公开访问指示符',
                    'BE':'编者',
                    'JI':'ISO来源文献名称缩写',
                    'OI':'ORCID标识符',
                    'J9':'长度为29个字符的来源文献名称缩写',
                    'PI':'出版商所在城市',
                    'Z9':'被引频次合计',
                    'PG':'页数',
                    'HO':'会议主办方',
                    'SU':'增刊',
                    'U1':'使用次数(最近180天)',
                    'UT':'入藏号',
                    'C1':'作者地址',
                    'SO':'出版物名称',
                    'DI':'数字对象标识符(DOI)',
                    'FX':'基金资助正文',
                    'NR':'引用的参考文献数',
                    'SN':'国际标准期刊号(ISSN)',
                    'SC':'研究方向',
                    'CY':'会议日期',
                    'PN':'子辑',
                    'CR':'引用的参考文献',
                    # 'VR':'版本号',
                    'AF':'作者全名',
                    'SP':'会议赞助方',
                    'GA':'文献传递号',
                    'EA':'提前访问日期',
                    'ID':'关键字',
                    'FU':'基金资助机构和授权号',
                    'CT':'会议标题',
                    'BF':'书记作者全名',
                    'HC':'ESI常被引用的论文仅适用于ESI订阅者',
                    'SE':'丛书标题',
                    'LA':'语种',
                    'VL':'卷',
                    'AU':'作者',
                    'RP':'通讯作者地址',
                    'PU':'出版商',
                    'U2':'使用次数(2013至今)',
                    'IS':'期',
                    'AB':'摘要',
                    'D2':'书籍的数字对象标识符(DOI)',
                    'TC':'Web of Secience 核心合集的被引频次计数',
                    'PA':'出版商地址',
                    'PM':'PubMed ID',
                    'AR':'文献编号',
                    'HP':'ESI热门论文',
                    'EI':'电子国际标准期刊号(eISSN)',
                    'EM':'电子邮件地址',
                    'DE':'作者关键词',
                    'EP':'结束页',
                    'BA':'书籍作者',
                    'PT':'出版物类型(J 期刊;B 书籍; S 丛书; P 专利',
                    'WC':'Web of Science类别',
                    'BN':'国际标准书号(ISBN)'}

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
