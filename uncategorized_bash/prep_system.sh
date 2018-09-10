#!/bin/bash

prev_system=/scratch/gpfs/dkozuch/phase_effects/1l2y/wtmd/amber03w_tip4p2005/annealed/1l2y_1bar_Vb_awtremd_v2/

cp -r $prev_system/run_files ./
cp -r $prev_system/optimal_frames ./
cp $prev_system/*.py ./
cp $prev_system/*.sh ./
cp $prev_system/*.cmd ./
cp $prev_system/temps.txt ./temps.txt

rm -r run_files/eq_files/ run_files/sim_files/ run_files/grompp_* run_files/#*
