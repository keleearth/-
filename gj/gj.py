#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

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
        #ID词汇表
        self.dataSet = set([])
        #数据集合
        self.yearData = {}
        #词集字典，方便确认位置
        self.dataDict = {}
        self.resultData = []
        #----找到数据中共有多少字段
        #self.dataSet = set(["DA"])
    #输出统计结果
    def stat(self,param):
       self.statData()
       statResultFile = "statResult.txt"
       if(len(param) > 0):
            statResultFile = param + "\\statResult.txt"
       with open(statResultFile, "w", encoding='utf-8') as statFile:
           statFile.write("word")
           for key in self.yearDataKeys:
               statFile.write("\t" + key)
           statFile.write("\t总计")
           statFile.write("\n")
           for dataList in self.resultData:
               for data in dataList:
                   statFile.write(str(data) + "\t")
               statFile.write("\n")
    def statData(self):
        self.readData()
        self.produceVocabSet()
        self.countYearWordNum()
        keys = self.yearData.keys()
        keys = list(keys)
        keys.sort()
        self.yearDataKeys = keys

        for i in range(len(self.dataSet)):
            dataList = [self.dataDict[i]]
            num = 0
            for key in keys:
                dataList.append(self.yearData[key][i])
                num = num + self.yearData[key][i]
            dataList.append(num)
            self.resultData.append(dataList)
        
    #实现替换文字
    def replace(self,param):
        #取出替换后文件位置
        #取出要替换的文字
        outputFileName = "replaceWordData.txt"
        statResultFile = "statResult.txt"
        if(len(param["outputFileName"]) > 0):
            outputFileName = param["outputFileName"] + "\\replaceWordData.txt"
        replaceWords = param["replaceWord"]
        with open(outputFileName, "w", encoding='utf-8') as outputFile, open(self.dataLocation, 'r', encoding='utf-8') as dataFile:
            
           for line in dataFile.readlines():
               for word in replaceWords:
                   line = line.replace(word,replaceWords[word])
               outputFile.write(line)
        print(param)
    #对词集进行编码方便确定位置
    def __encodedDataSet(self):
        index = 0
        for dictKey in self.dataSet:
            self.dataDict[dictKey] = index
            self.dataDict[index] = dictKey
            index = index + 1

    #根据词集和数据集合统计个数
    def countYearWordNum(self):
        self.__encodedDataSet()
        for key in self.yearData:
            #每一年的数据集
            #print(key)
            self.yearData[key] = self.__count(self.yearData[key])
    
    def __count(self,yearData):
        
        dataCount = [0]*len(self.dataSet)
        for data in yearData:
            if(data in self.dataSet):
                dataCount[self.dataDict[data]
                          ] = dataCount[self.dataDict[data]] + 1
        return dataCount


    #对ID列进行分词并生成词表和每一年的词集
    def produceVocabSet(self):
        for vocab in self.data:
            if 'ID' in vocab and 'PY' in vocab:
                #print(vocab['ID'])
                yearDataList = vocab["ID"].strip().replace("_\t_", " ").split(";")
                #print(yearDataList)
                yearKey = vocab.get('PY',"1970")
                if yearKey in self.yearData:
                    #每一年的数据集
                    self.yearData[yearKey].extend(yearDataList)
                else:
                    self.yearData[yearKey] = yearDataList
            #     print(vocab["ID"].replace("_\t_", ";").split(";"))
                #词表集合
                self.dataSet = self.dataSet | set(yearDataList)
    #读取文件中数据 
    def readData(self):
        with open(self.dataLocation, 'r',encoding='utf-8') as dataFile:
            # for line in dataFile.readlines():
            #     print(line)
            dataFile.readline()
            dataFile.readline()
            while True:
                oneData = self.__readOneData(dataFile)
                if(oneData):
                    self.data.append(oneData)
                else:
                   break
    #只读取数据文件中的一条数据
    def __readOneData(self, dataFile):
        #每一条记录的数据结构
        dataStruct = {}
        line = dataFile.readline()
        #数据结构每一字段包含的数据
        column=""
        cloumnData=""
        #cloumnData=[]
        while line:
            if(line.startswith('\n')):
                break
            else:
                if(line.startswith(' ')):
                    dataStruct[column] = dataStruct[column] + "_\t_" + line[3:].strip('\n')
                    #dataStruct[column].append(line[3:].strip('\n'))
                else:
                    column = line[0:2]
                    cloumnData = line[3:].strip('\n')
                    #cloumnData = [line[3:].strip('\n')]
                    dataStruct[column] = cloumnData
                    #self.dataSet.add(column)
                # self.data.append(line)
                line = dataFile.readline()
        return dataStruct
        
    # #找到数量最多的单词
    # def searchTopWords(self,num):
    #     #将各年度数据相加得到数量
    #     totalNum = np.zeros(len(self.dataSet), int)
    #     for yearData in self.yearData:
    #         totalNum = totalNum + np.array(self.yearData[yearData])
    #     wordList = []
    #     #数组长度
    #     length = len(totalNum)
    #     #拿到数量前100的词汇集合
    #     if length < num:
    #         wordList =[]
    #     else:    
    #         wordListIndex = np.argpartition(totalNum, 0 - num)
    #         for i in range(0,num):
    #             wordList.append(self.dataDict[wordListIndex[length-1-i]])

    #     #print(totalNum)
    #     return wordList

    # #处理汇总后的数据数据
    # def dealData(self, wordList):
    #     resultData = []
    #     # columunDataName = ['year']
    #     # columunDataName.extend(wordList)
    #     # resultData.append(columunDataName)
    #     for oneYearData in self.yearData:
    #         dataList = self.__dealOneYearData(self.yearData[oneYearData],wordList)
    #         dt = []
    #         dt.append(oneYearData)
    #         dt = dt+dataList 
    #         resultData.append(dt)
    #     self.resultData = resultData
    #    # return resultData

    # def __dealOneYearData(self,oneYearData,wordList):
    #     dataList = [] 
    #     for word in wordList:
    #         #print(self.dataDict[word])
    #         index = self.dataDict[word]
    #         #print(index)
    #         dataList.append(oneYearData[index])
    #     return dataList
    #根据num调整尺寸
    def figsize(self,num):
        figsize = (7.5,6.8)
        if(num > 50 and num < 70):
            figsize = (7.5,7.8)
        if(num >= 70):
            figsize = (9,9.8)
        return figsize

    #使用pandas对数据进行可视化
    def showData(self,num):
        columunDataName = ['word']
        for key in self.yearDataKeys:
            columunDataName.append(key)
        columunDataName.append("total")
        dataFrame = pd.DataFrame(self.resultData, columns=columunDataName)
        mpl.rcParams['font.sans-serif'] = ['SimHei','FangSong', 'KaiTi'
                                           ]  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
        mpl.rcParams['font.size'] = 12  # 字体大小
        mpl.rcParams['axes.unicode_minus'] = False
        dataFrame = dataFrame.sort_values(by="total",ascending=False)
        
        dataFrame = dataFrame.iloc[0:num,0:]
        #开始画图
        fig, ax = plt.subplots(figsize=self.figsize(num))
        
        ax.set_yticklabels(dataFrame["word"])
        ax.set_yticks(range(len(dataFrame["word"])))
        ax.set_ylabel('单词')
        ax.set_xlabel('年份', loc='right', labelpad=5)
        ax.set_xticklabels(dataFrame.columns.tolist()[1:-1])
        ax.set_xticks(range(len(dataFrame.columns.tolist()[1:-1 ])))
        #ax.grid(True)
        ax.tick_params(axis='x', rotation=70)
        ax.tick_params(axis='y', rotation=10)
        ax.pcolor(dataFrame.iloc[0:, 1: -1], edgecolors='k', linewidths=1)
        im = plt.imshow(dataFrame.iloc[0:-1, 1: -1])
        plt.colorbar(im)
        return fig
        # plt.show()

if __name__ == '__main__':
    actuator = Actuator('E:\\project\\python\\data.txt')
    actuator.statData()
    
    # actuator.showData(30)
    # actuator.showData(50)
    actuator.showData(100)
   

    # print("aa")
