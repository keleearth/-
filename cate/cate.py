#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#朴素贝叶斯分类算法

#收集训练数据
#返回文档数据和标签
def loadDataSet():
    return[[ " my ","dog ", " has ", " flea ", " problems ", " help ", " please "],
        [" maybe ","not ", " take ", "him ", "to ", "dog ", "park", "stupid"],
        [" my ", " dalmatione","is", " so ", "cute", "I", " love ", " him "],
        [ " stop " , "posti","stupid"," worthless ", " garbage "],
        [ "mr ","licks "," ate t"," my" ,"stea k ", " how ", "to ", " stop ", " him "],
        [" quit ", " buying ", " worthless "," F"," dog ","food ", "stupid"]],[0,1,0,1,0,1]

#遍历训练集中的文本生成词汇表
def vocabList(dataSet):
    vocabSet = set([])
    for doc in dataSet:
        vocabSet = vocabSet | set(doc)
    return list(vocabSet)
#根据词汇表生成文档词集模型
def wordsVec(vocabList,inputText):
    textVec = [0]*len(vocabList)
    for word in inputText:
        if word in vocabList:
            textVec[vocabList.index(word)] = 1
    return textVec

from numpy import *
from numpy.core._multiarray_umath import log
#训练算法 参数  训练文档 训练文档类别
def train(trainDoc,trainDocCategory):
    #计算文档数量
    trainDocNum = len(trainDoc)
    #计算文档中侮辱性文档出现的概率
    pInsultingDoc = sum(trainDocCategory) / float(trainDocNum)

    #文档中单词总量
    wordsNum = len(trainDoc[0])
    #构建类别1和类别2的向量空间
    p1Vec = ones(wordsNum)
    p2Vec = ones(wordsNum)
    #分别计算类别1和类别2的单词总数
    p1Num = 2.0
    p2Num = 2.0
    #遍历训练文档
    for i in range(trainDocNum):
        #判断是否是类别1的文档
        if trainDocCategory[i] == 1:
            #计算侮辱性文档中每个单词出现的次数
            p1Vec += trainDoc[i]
            #计算侮辱性文档中所有单词总量
            p1Num += sum(trainDoc[i])
        else:
            p2Vec += trainDoc[i]
            p2Num += sum(trainDoc[i])
    #计算类别1和类别2下各单词出现的概率
    #p1 = log(p1Vec / p1Num)
    #p2 = log(p2Vec / p2Num)
    p1 = p1Vec / p1Num
    p2 = p2Vec / p2Num
    return pInsultingDoc,p1,p2


data1, data2 = loadDataSet()
wordsList = vocabList(data1)
#print(wordsList)
#textVec = wordsVec(wordList)
docVec = []
for i in range(len(data1)):
    docVec.append(wordsVec(wordsList, data1[i]))
    #训练数据
pInsultingDoc, p1, p2 = train(array(docVec), array(data2))
#print(docVec)
#print(pInsultingDoc)
print(p1)
print(p2)
#print(where(p1==max(p1)))
#print(where(p2==max(p2)))
#对文档进行分类
#textDoc 要分类的文档向量
#p1 侮辱性文档下的各单词概率列表
#p2 正常文档下各单词的概率列表
#pInsultingDoc 侮辱文档的概率

def classifyDoc(textDoc,p1,p2,pInsultingDoc):
    
    p1 = sum(textDoc*p1) + log(pInsultingDoc)
    p2 = sum(textDoc*p2) + log(1-pInsultingDoc)

    print("p1的概率为" + str(p1))
    print("p2的概率为" + str(p2))
    cateNum = 1
    if(p1> p2):
        cateNum = 1
    if(p2 > p1):
        cateNum = 2
    return cateNum

#测试训练数据

def testTrain():
    #加载数据集
    docs,classes = loadDataSet()
    #创建词汇表
    wordsList = vocabList(docs);
    #构建训练数据的向量空间
    docVec = []
    for doc in docs:
        docVec.append(wordsVec(wordsList, doc))
    #训练数据
    pInsultingDoc, p1, p2 = train(array(docVec), array(classes))
    #测试数据
    testDoc = ["stupid"]
    #构建测试数据词向量
    testDocVec = array(wordsVec(wordsList, testDoc))
    cate = classifyDoc(testDocVec,p1,p2,pInsultingDoc)
    print("类别是" + str(cate))
testTrain()
