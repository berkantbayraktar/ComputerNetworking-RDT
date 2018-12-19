#!/usr/bin/env python
# -*- coding: utf-8 -*- 

big_file = open("demofile.txt","r")
little_file = open("demofile_light.txt","w+")
counter = 10000
for i in range(0,1500):
    line = big_file.readline()
    little_file.write(line)
    counter-=1
    if(counter == 0):
        break