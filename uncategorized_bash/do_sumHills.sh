#!/bin/bash

parallel=True
sims=27 #sims minus one since labeling starts at zero

plumed=/home/dkozuch/programs/plumed_241/bin/plumed
readarray rep_temps < temps.txt

property=potential
#stride=10000

mkdir fes_${property}_files

if [ "$parallel" = "True" ]; then
	for i in $(seq 0 $sims)
	do
		( t=${rep_temps[$i]}
		t=$(echo "$t" | bc) #some whitespace issues
		kt=$(echo "$t*0.008314" | bc)
		echo $i
		$plumed sum_hills --hills hills.${i} --outfile fes_${property}_${i}.dat --mintozero > tmp 2>&1 ) &
	done
	wait
else
	for i in $(seq 0 $sims)
	do
		t=${rep_temps[$i]}
		t=$(echo "$t" | bc) #some whitespace issues
		kt=$(echo "$t*0.008314" | bc)
		echo $i
		$plumed sum_hills --hills hills.${i} --outfile fes_${property}_${i}.dat --mintozero > tmp 2>&1
	done
fi

mv fes_${property}_*.dat fes_${property}_files


