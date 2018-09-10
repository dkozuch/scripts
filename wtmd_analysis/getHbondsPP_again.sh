#!/bin/bash

#assumes ${property} for the system has been calculated to some time before
#this calculates the ${property} for the remaining time in the simulation

protein=1l2y
gmx=gmx_164_pd241
nreps=27 #counting from 0

property=hbonds_pp
folder=${property}_files

for i in $(seq 0 $nreps); do

( echo "Performing analysis for system number: "$i

#find out last time calculated previously
filename=${folder}/${property}_${i}.xvg
last=$(tail -n 1 $filename)
lastArray=($last)
lastTime=${lastArray[0]}
if [[ $lastTime = *"e"* ]]; then
	echo "Found scientific notation. Converting..."
	lastTime=$(printf "%.5f" $lastTime)
fi
echo "Last time found in file ("$filename"): "$lastTime
newTime=$(echo "$lastTime+1" | bc)
echo "Starting from new time: "$newTime

#get property
newFilename=${property}_${i}_new.xvg
logfile=tmp_${property}_log_${i}.txt
$gmx hbond -f ${protein}_sim_${i}.xtc -s TOPO_SIM/${protein}_sim_${i}.tpr -b ${newTime} -num ${newFilename} > ${logfile} 2>&1 << EOF
1
1
EOF

#cut out comments, concatenate, and replace
echo "Concatenating and replacing..."
sed -E '/^#|^@/ d' $newFilename > tmp_${property}_${i}.xvg
cat $filename tmp_${property}_${i}.xvg > tmp_${property}2_${i}.xvg
cp tmp_${property}2_${i}.xvg $filename
rm $newFilename tmp_${property}_${i}.xvg tmp_${property}2_${i}.xvg ${logfile} 
) &

done
wait
