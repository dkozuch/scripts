#!/bin/bash

protein=1l2y

gmx=gmx_164_gpu_pd241
basefiles="eq.mdp sim.mdp topol.top ${protein}_min.gro"
tRef=300

#sh getAnnealedFrames.sh

#rm -r TOPO
mkdir TOPO_EQ

readarray rep_temps < temps.txt
num_reps=${#rep_temps[*]}

cd run_files
mkdir eq_files
mkdir sim_files

#copy files
for i in $(seq 1 $num_reps); do
echo $i

index=$(echo "$i-1" | bc )  #bash arrays start counting at zero
t=${rep_temps[$index]}
t=$(echo "$t" | bc) #some whitespace issues

sed -i '/ref-t/c\ref-t = '$t' '$t'; edited by dkozuch' eq.mdp
sed -i '/^continuation/c\continuation = no; edited by dkozuch' eq.mdp
sed -i '/gen-vel/c\gen-vel = yes; edited by dkozuch' eq.mdp
sed -i '/gen-temp/c\gen-temp = '$t'; edited by dkozuch' eq.mdp
cp eq.mdp eq_files/eq_${index}.mdp

sed -i '/ref-t/c\ref-t = '$t' '$t'; edited by dkozuch' sim.mdp
sed -i '/gen-vel/c\gen-vel = no; edited by dkozuch' sim.mdp
sed -i '/^continuation/c\continuation = yes; edited by dkozuch' sim.mdp
sed -i '/gen-temp/c\gen-temp = '$t'; edited by dkozuch' sim.mdp
cp sim.mdp sim_files/sim_${index}.mdp

if (( $(bc <<< "$t < $tRef") )); then
	${gmx} grompp -f eq_files/eq_${index}.mdp -c ../annealed_frames/${protein}_frame_${t}K.gro -p topol.top -o ${protein}_eq_${index}.tpr -maxwarn 1 > grompp_eq.txt 2>&1
	rm \#*
else
	${gmx} grompp -f eq_files/eq_${index}.mdp -c ${protein}_min -p topol.top -o ${protein}_eq_${index}.tpr -maxwarn 1 > grompp_eq.txt 2>&1
	rm \#*
fi

mv ${protein}_eq_${index}.tpr ../TOPO_EQ/

done
