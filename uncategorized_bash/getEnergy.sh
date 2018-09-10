#!/bin/bash

protein=1l2y
gmx=gmx_164_pd

property=$1

mkdir ${property}_files

for i in $(seq 0 27)
do
( echo $i
$gmx energy -f ${protein}_sim_${i} -o ${property}_${i}.xvg <<EOF
$property
EOF
mv ${property}_${i}.xvg ${property}_files/ ) &
done
wait

echo "Done"
