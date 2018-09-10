#!/bin/bash

protein=1l2y
gmx=gmx_164_gpu_pd241
begin=0

property=potential
mkdir ${property}_files

for i in $(seq 0 27); do
echo $i

$gmx energy -f ${protein}_eq_${i} -o ${property}_${i}.xvg -b $begin > tmp.txt 2>&1 << EOF
${property}
0
EOF
mv ${property}_$i.xvg ${property}_files/

done

