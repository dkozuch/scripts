#!/bin/bash

protein=1l2y

gmx=gmx_164_gpu_pd241
tRef=300

mkdir annealed_frames
readarray rep_temps < temps.txt
num_reps=${#rep_temps[*]}
echo "Number of replicas: "$num_reps

cd annealing

for i in $(seq 1 $num_reps); do

index=$(echo "$i-1" | bc )  #bash arrays start counting at zero
t=${rep_temps[$index]}
t=$(echo "$t" | bc) #some whitespace issues
echo $index" "$t

if [ $(echo $t '<' $tRef | bc) -eq 1 ]; then #bash can't handle floats so use bc
tns=$(echo "scale=3; $tRef - $t" | bc)
tps=$(echo "$tns*1000" | bc)
echo $tps
${gmx} trjconv -f ${protein}_sim.xtc -s ${protein}_sim.tpr -b $tps -e $tps -o ${protein}_frame_${t}K.gro > tmp 2>&1 << EOF
0
EOF
mv ${protein}_frame_${t}K.gro ../annealed_frames
fi

done
