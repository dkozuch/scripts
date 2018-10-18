#!/bin/bash

#SBATCH --nodes=1
# --mem=5120
#SBATCH -C broadwell
#SBATCH --ntasks-per-node=8
#SBATCH --sockets-per-node=1
# --gres=gpu:1
# --gres-flags=enforce-binding
#SBATCH -t 24:00:00
# sends mail when process begins, and
# when it ends. Make sure you define your email
# address.
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-type=fail
#SBATCH --mail-user=dkozuch@princeton.edu
#SBATCH --array=1-42:8

gmx=gmx_164
mol=sds
cutoff=0.3
dt=1
b=0
e=1000000

idb=$SLURM_ARRAY_TASK_ID
num=7 #number of atom indexes to run in per array task, minus 1
ide=$(echo "$idb + $num" | bc)

echo "Start atom index: "$idb
echo "Stop atom index:"$ide

for i in $(seq $idb $ide); do #188 total
(
echo $i
$gmx select -f ${mol}_sim -s ${mol}_sim -os count_${cutoff}nm_id${i} -select 'name OW and within '${cutoff}' of atomnr '${i}'' -b $b -e $e -dt $dt > tmp_count.log 2>&1
) & #do in parallel
done
wait
