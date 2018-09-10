#!/bin/bash

#get old colvar/hills files for continuation after 2,450,000 ps
#for some reason number of lines is weird but seems to work

for i in $(seq 0 27); do
echo "Copying colvar."${i}
head -n 2450837 ../wtmd_unfolded/colvar.${i} > colvar.${i}
done

for i in $(seq 0 27); do
echo "Copying hills."${i}
head -n 2450871 ../wtmd_unfolded/hills.${i} > hills.${i}
done

