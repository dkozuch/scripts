#!/bin/bash

gmx=gmx_164_gpu_pd241
protein=1l2y
time=2450

mkdir TOPO_SIM

for i in $(seq 0 27); do

$gmx grompp -f run_files/sim_files/sim_${i}.mdp -c frames/${protein}_sim_${i}_${time}ns.gro -p run_files/topol.top -o ${protein}_sim_${i}.tpr -maxwarn 1
mv ${protein}_sim_${i}.tpr TOPO_SIM/

done 
