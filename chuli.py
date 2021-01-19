#!/usr/bin/env python
# -*- coding: UTF-8 -*-


try:
    file = open("Integron.blast-1", 'r')
    file2 = open("Integron.blast-2",'w')
    for line in file.readlines():
        words = line.split("\t")
        d3l = words[2]
        d4l = words[3]
        if float(d3l) >= 90 and int(d4l) >= 90 :
            print(line)
            file2.write(line)
    
finally:
    file.close()
