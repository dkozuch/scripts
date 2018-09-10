#!/bin/bash

protein=1l2y
gmx=gmx_164_pd241

#rm -r rms_results
mkdir rmsd_files

for i in $(seq 0 27); do
(echo $i

#use pdb structure as reference
$gmx rms -f ${protein}_sim_${i} -s run_files/${protein}_min.tpr -o rmsd_$i -b 0 > tmp1.txt 2>&1 << EOF
3
3
EOF
mv rmsd_$i.xvg rmsd_files

done
wait
