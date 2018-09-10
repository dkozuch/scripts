#!/bin/bash

#assumes rmsd for the system has been calculated to some time before
#this calculates the rmsd for the remaining time in the simulation

protein=1l2y
gmx=gmx_164_pd241
nsims=27 #counting from 0

property=rmsd
folder=${property}_files

for i in $(seq 0 $nsims); do

( 
echo "Performing analysis for system number: "$i

#find out last time calculated previously
filename=${folder}/${property}_${i}.xvg
last=$(tail -n 1 $filename)
lastArray=($last)
lastTime=${lastArray[0]}
echo "Last time found in file ("$filename"): "$lastTime
newTime=$(echo "$lastTime+1" | bc)
echo "Starting from new time: "$newTime

#get property
newFilename=${property}_${i}_new.xvg
${gmx} rms -f ${protein}_sim_${i}.xtc -s run_files/${protein}_min.tpr -b $newTime -o ${newFilename} > tmp_rmsd_${i}_log.txt 2>&1  <<EOF
3
3
EOF

#cut out comments, concatenate, and replace
echo "Concatenating and replacing..."
sed -E '/^#|^@/ d' $newFilename > tmp_rmsd_${i}.xvg
cat $filename tmp_rmsd_${i}.xvg > tmp_rmsd2_${i}.xvg
cp tmp_rmsd2_${i}.xvg $filename
rm $newFilename tmp_rmsd_${i}.xvg tmp_rmsd2_${i}.xvg tmp_rmsd_${i}_log.txt 
) &

done
wait
