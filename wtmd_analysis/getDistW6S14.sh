#!/bin/bash

protein=1l2y
gmx=gmx_164_pd241

property=dist614 #minimum distance residue 6 to residue 14

mkdir ${property}_files

for i in $(seq 0 27)
do
( echo $i
ref="resnr 6"
sel="resnr 14"
$gmx pairdist -f ${protein}_sim_${i} -s ${protein}_sim_${i} -o ${property}_${i} -selgrouping res -ref "$ref" -sel "$sel" > tmp_${property}.log 2>&1
mv ${property}_${i}.xvg ${property}_files/ ) &
done
wait

echo "Done"
