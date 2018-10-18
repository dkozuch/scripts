#!/bin/bash
#SBATCH -N 1
#SBATCH -J HBond
#SBATCH --ntasks-per-node=8
### -#SBATCH --mem-per-cpu=12000MB
#SBATCH -t 24:00:00
#SBATCH --mail-user=buralcan@princeton.edu
#SBATCH --mail-type=end

./betul.ex sample.gro no 2 #> LSI_unfolded_5kBar.txt
cp LSI_op.txt LSI_op6.txt
rm LSI_op.txt

