#!/usr/bin/env python
# -*- coding: UTF-8 -*-


try:
    file = open("Integron.blast-2", 'r')
    file2 = open("tj1.txt", 'w')
    dict = {}
    for line in file.readlines():
        words = line.split("\t")
        d2l = words[1]
        if d2l in dict.keys():
            dict[d2l] = dict[d2l] + 1
        else:
            dict[d2l] = 1
    dictKeys = sorted(dict.keys())
    for key in dictKeys:
        #print(key) 
        file2.write(key + "\t" + str(dict[key]) + "\n")
    #print(dict)

finally:
    file.close()
