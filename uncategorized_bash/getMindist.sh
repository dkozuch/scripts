#!/bin/bash

protein=1l2y
gmx=gmx_164_pd

mkdir mindist_files

for i in $(seq 0 27)
do
( echo $i
$gmx mindist -f ${protein}_sim_${i} -s TOPO_SIM/${protein}_sim_${i} -n dist_index.ndx -od mindist_${i}.xvg <<EOF
18
19
EOF
mv mindist_${i}.xvg mindist_files/ ) &
done
wait

echo "Done"
