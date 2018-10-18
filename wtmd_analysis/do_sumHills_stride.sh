#!/bin/bash

sims=27 #sims minus one since labeling starts at zero

plumed=/home/dkozuch/programs/plumed_242/bin/plumed
readarray rep_temps < temps.txt

property=potential
stride=100000

folder=fes_${property}_files_stride
mkdir $folder

for i in $(seq 0 $sims); do
	( t=${rep_temps[$i]}
	t=$(echo "$t" | bc) #some whitespace issues
	kt=$(echo "$t*0.008314" | bc)
	echo $i
	$plumed sum_hills --hills hills_clean/hills_clean.${i} --outfile fes_${property}_${i}. --mintozero --stride $stride > tmp_fes_${property}_${i}.txt 2>&1 ) &
	done
	wait

#rm tmp_fes_${property}_*
mv fes_${property}_*.dat ${folder}/


