#!/bin/bash

protein=1l2y
gmx=gmx_164_pd241
property=$1
folder=${property}_files
b=0
e=100000 #force write to file for testing

mkdir ${folder}

for i in $(seq 0 27); do
(echo $i

outfile=${property}_${i}.xvg
logfile=tmp_${property}_log_${i}.txt

$gmx energy -f ${protein}_sim_${i}.edr -o ${outfile} -b $b -e $e > ${logfile} 2>&1 << EOF
$property
0
EOF
mv ${outfile} ${folder}/
rm ${logfile}
) &

done
wait
