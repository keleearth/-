#!/usr/bin/env python
# -*- coding: UTF-8 -*-

with open("Integron.blast-1", 'r') as file1, open("Integron.blast-2", 'w') as file2, open("tj1.txt", 'w') as file3:
    #存放统计结果
    dict = {}
    for line in file1.readlines():
        words = line.split("\t")
        d2l = words[1]
        d3l = words[2]
        d4l = words[3]
        #筛选条件
        if float(d3l) >= 90 and int(d4l) >= 90:
            #将筛选后数据写到文件中
            file2.write(line)
            #对数据进行统计，字典中存在此数据 值加一，不存在，添加进去，值为1
            if d2l in dict.keys():
                dict[d2l] = dict[d2l] + 1
            else:
                dict[d2l] = 1
    #对字典中的结果进行值排序
    dictKeys = sorted(dict.keys())
    #将统计结果写进文件
    for key in dictKeys:
        file3.write(key + "\t" + str(dict[key]) + "\n")
# try:
#     #原始数据
#     file1 = open("Integron.blast-1", 'r')
#     #筛选后的数据存放位置
#     file2 = open("Integron.blast-2", 'w')
#     #存放统计结果的文件
#     file3 = open("tj1.txt", 'w')
#     #存放统计结果
#     dict = {}
#     for line in file1.readlines():
#         words = line.split("\t")
#         d2l = words[1]
#         d3l = words[2]
#         d4l = words[3]
#         #筛选条件
#         if float(d3l) >= 90 and int(d4l) >= 90:
#             #将筛选后数据写到文件中
#             file2.write(line)
#             #对数据进行统计，字典中存在此数据 值加一，不存在，添加进去，值为1
#             if d2l in dict.keys():
#                 dict[d2l] = dict[d2l] + 1
#             else:
#                 dict[d2l] = 1
#     #对字典中的结果进行值排序
#     dictKeys = sorted(dict.keys())
#     #将统计结果写进文件
#     for key in dictKeys:
#         file3.write(key + "\t" + str(dict[key]) + "\n")
# finally:
#     file1.close()
#     file3.close()
#     file3.close()
