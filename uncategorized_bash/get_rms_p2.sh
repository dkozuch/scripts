#!/bin/bash

protein=1l2y
gmx=gmx_164_gpu_pd241

mkdir rmsd_files

for i in $(seq 0 0); do
#(echo $i

#use pdb structure as reference
$gmx rms -f ${protein}_sim_${i} -s run_files/${protein}_min.tpr -o rmsd_$i > tmp1.txt 2>&1 << EOF
3
3
EOF

tail -n +19 rmsd_$i.xvg > rmsd_${i}_tail.xvg #remove comments at beginning of file
cat prev_rmsd_files/rmsd_$i.xvg rmsd_${i}_tail.xvg > rmsd_${i}_new.xvg
mv rmsd_${i}_new.xvg rmsd_files/rmsd_${i}.xvg

#) &

done
wait
