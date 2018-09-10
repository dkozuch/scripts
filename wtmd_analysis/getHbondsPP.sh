#!/bin/bash

protein=1l2y
gmx=gmx_164_pd241
property=hbonds_pp #protein-protein hbonds
folder=${property}_files
b=0
e=100000 #force write to file for testing

mkdir ${folder}

for i in $(seq 0 27); do
(echo $i

#protein-protein hbonds
outfile=${property}_${i}.xvg
logfile=tmp_${property}_log_${i}.txt

$gmx hbond -f ${protein}_sim_${i}.xtc -s TOPO_SIM/${protein}_sim_${i}.tpr -num ${outfile} -b $b -e $e > ${logfile} 2>&1 << EOF
1
1
EOF
mv ${outfile} ${folder}/
rm ${logfile}
) &

done
wait
