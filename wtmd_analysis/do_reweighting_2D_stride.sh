#!/bin/bash

#idea is to calculate reweighted values over sequential time blocks like the sum_hills stride option (1-100ns, 1-200ns, 1-300ns, etc.)
#basically grab portions of files useing head command

nsims=27 #counting from zero
stride=100000

readarray rep_temps < temps.txt
property1=$1
property2=$2
echo "Doing 2D reweighting for: "${property1}" and "${property2}
folder=reweighted_${property1}_${property2}_stride
mkdir $folder

#get biasfactor from plumed/plumed_PT.0 to make sure things match
str=$(sed -n -e '/^LABEL=metad/p' plumed/plumed_PT.0.dat)
bsf=$(echo $str | awk 'BEGIN {FS="BIASFACTOR="} {print $2}')
bins=1000

#if statement makes sure we only proceed if output file doesn NOT already exist
#keeps us from recalculating stuff over and over which can be slow

#for i in $(seq 0 $nsims); do
for i in 22; do
(
t=${rep_temps[$i]}
t=$(echo "$t" | bc) #some whitespace issues
kt=$(echo "$t*0.008314" | bc)

	#determine number of strides to do
	colvar_file=${property1}_${property2}_colvar/${property1}_${property2}_colvar.${i}
	lines=$(wc -l < $colvar_file) #should give number of lines in the file
	nstrides=$(echo "${lines}/${stride}" | bc) #bc automatically rounds down
	echo "Number of lines in colvar file: "$lines
	echo "Number of strides: "$nstrides

	#for j in $(seq 0 $nstrides); do
	for j in 40; do
	if [ ! -f ${folder}/reweighted_${property1}_${property2}.${i}.${j} ]; then
	block=$(echo "${stride}*(${j}+1)" | bc)
	echo $property1 $property2 $i $j $block
	head -n $block ${colvar_file} > tmp_${property1}_${property2}_colvar.${i}.${j}
	reweight.py -bsf $bsf -kt $kt -fpref fes_potential_files_stride/fes_potential_${i}.${j} -bin $bins -nf 1 -fcol 2 -colvar tmp_${property1}_${property2}_colvar.${i}.${j} -biascol 6 -rewcol 2 4 -outfile reweighted_${property1}_${property2}.${i}.${j} -v > tmp_log.txt 2>&1 
	mv reweighted_${property1}_${property2}.${i}.${j} ${folder}/
	rm tmp_${property1}_${property2}_colvar.${i}.${j}
	fi
	done
) &

done
wait

