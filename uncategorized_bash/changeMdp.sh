#!/bin/bash

protein=1l2y
gmx=gmx_164_gpu_pd241

cd TOPO_SIM/

for i in $(seq 0 27); do
$gmx grompp -f ../run_files/sim_files/sim_${i}.mdp -c ${protein}_sim_${i}.tpr -p ../run_files/topol.top -t ../${protein}_sim_${i}.cpt -o ${protein}_sim_${i}
done
