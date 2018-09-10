#!/bin/bash

protein=1l2y
gmx=gmx_164_gpu_pd241
begin=100000

#rm -r rms_results
mkdir rmsd_files
mkdir rmsf_files

for i in $(seq 0 27); do
(echo $i

#use pdb structure as reference
$gmx rms -f ${protein}_sim_${i} -s run_files/${protein}_min.tpr -o rmsd_$i -b 0 > tmp1.txt 2>&1 << EOF
3
3
EOF
mv rmsd_$i.xvg rmsd_files

#mpirun -n 1 $gmx rmsf -f ${protein}_sim -s ${protein}_sim -o rmsf_$i.xvg -b $begin > tmp2.txt 2>&1 << EOF
#2
#EOF
#mv rmsf_$i.xvg rmsf_files
) &

done
wait
