#!/bin/bash

gmx=gmx_164_gpu_pd241
protein=1l2y
cpt_folder=prev_cpt
old_topo_folder=old_TOPO_SIM
new_topo_folder=TOPO_SIM
nsims=27 #count from 0
dt=0.002

rm -r $new_topo_folder
mkdir $new_topo_folder

#get last time/step from checkpoint file 0
echo "Getting time from cpt file"
$gmx dump -cp ${cpt_folder}/${protein}_sim_0.cpt > tmp.txt 2>&1
line=$(sed -n -e '/^t =/p' tmp.txt)
t=$(echo $line | cut -d " " -f 3)
echo "Time = "$t
step=$(echo "${t}/${dt}" | bc)
echo "dt = "$dt
echo "Step = "$step 

#edit step in mdp files
echo "Editing mdp files ..."
for i in $(seq 0 $nsims); do 
sed -i '/^init-step/c\init-step = '$step'' run_files/sim_files/sim_${i}.mdp
done

#make new tpr files
echo "Making new tpr files..."
for i in $(seq 0 $nsims); do 
$gmx grompp -f run_files/sim_files/sim_${i}.mdp \
	-c ${old_topo_folder}/${protein}_sim_${i}.tpr \
	-t ${cpt_folder}/${protein}_sim_${i}.cpt \
	-p run_files/topol.top \
	-o ${new_topo_folder}/${protein}_sim_${i}.tpr

done
