#!/bin/bash

protein=1l2y
gmx=gmx_164
nsims=27

#command line takes two arguments - one for each group
group1=$1
group2=$2
property=hbonds_${group1}_${group2} #group1 group2 hbonds
folder=${property}_files
b=0
e=100000 #force write to file for testing

mkdir ${folder}

for i in $(seq 0 $nsims); do
(echo $i

outfile=${property}_${i}.xvg
logfile=tmp_${property}_log_${i}.txt

$gmx hbond -f ${protein}_sim_${i}.xtc -s TOPO_SIM/${protein}_sim_${i}.tpr -n index -num ${outfile} -b $b -e $e > ${logfile} 2>&1 << EOF
${group1}
${group2}
EOF
mv ${outfile} ${folder}/
#rm ${logfile}
) &

done
wait
