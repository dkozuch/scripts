#!/bin/bash

readarray rep_temps < temps.txt
mkdir reweighted_rmsd

bsf=10
bins=100
#fes_version=2

for i in $(seq 0 27); do
(t=${rep_temps[$i]}
t=$(echo "$t" | bc) #some whitespace issues

kt=$(echo "$t*0.008314" | bc)
reweight.py -bsf $bsf -kt $kt -fpref fes_potential_files/fes_potential_${i} -bin $bins -nf 1 -fcol 2 -colvar rmsd_colvar/rmsd_colvar.${i} -biascol 2 -rewcol 1 -outfile reweighted_rmsd.${i} -v 
mv reweighted_rmsd.${i} reweighted_rmsd/ ) &

done
wait

