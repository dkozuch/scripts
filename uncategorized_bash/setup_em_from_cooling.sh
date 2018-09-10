#!/bin/bash

#protein name
protein=1aki
#number of proteins in powder
#n=8

#input
temp_begin=300 #Kelvin
temp_end=0 #Kelvin
temp_interval=20 #degress Kelvin to separate each frame
cooling_rate=0.01 #K/ps

rootdir=/scratch/gpfs/dkozuch
dir=${rootdir}/potential_energy_landscapes/lyzozyme2/protein_powder_04/cool_from_300

#basefiles
mdp="npt"
basefiles=${mdp}".mdp topol.top parallel.cmd"

#number of frames, assumes integer
temp_range=$(echo "scale=0; ${temp_begin} - ${temp_end}" | bc)
n_frames=$(echo "scale=0; ${temp_range}/${temp_interval}" | bc)

#make folder for files
mkdir em

for i in $(seq 0 ${n_frames})
do

#get temp
temp=$(echo "${temp_begin}-(${i}*${temp_interval})" |bc)
echo ${temp}

cd em
mkdir ${temp}
cd ../

#get time
frame_time=$(echo "${i}*${temp_interval}/${cooling_rate}" | bc)

#get frame, 0 is for whole system
mpirun -n 1 gmx_514 trjconv -f ${protein}_nvt_cool.xtc -s ${protein}_nvt_cool.tpr -b ${frame_time} -e ${frame_time} -o ${protein}_coolt${temp}.gro > tmp_gmx.txt 2>&1 <<EOF
0
EOF

cp ${protein}_coolt${temp}.gro ./em/${temp}/
rm ${protein}_coolt${temp}.gro
cp ${basefiles} ./em/${temp}/
cd em/${temp}

#edit mdp file: sed -i '/string in line you want to replace/c\strng to replace that line' file
sed -i '/ref-t/c\ref-t = '${temp}'' ${mdp}.mdp
sed -i '/gen-temp/c\gen-temp = '${temp}'' ${mdp}.mdp
 
#maxwarn 1 for velocity generation using Parrinello-Rahman barostat; should be okay since system is already decently equilibrated
mpirun -n 1 gmx_514 grompp -f ${mdp} -c ${protein}_coolt${temp}.gro -p topol.top -o ${protein}_coolt${temp}_${mdp} -maxwarn 1 > grompp_output.txt 2>&1
 
#edit sbatch file
sed -i '/cd/c\cd '${dir}'/em/'${temp}'' parallel.cmd
sed -i '/srun gmx_514 mdrun -tunepme yes -deffnm '${protein}'_nvt_cool/c\srun gmx_514 mdrun -tunepme yes -deffnm '${protein}'_coolt'${temp}'_'${mdp}'' parallel.cmd
mv parallel.cmd parallel_coolt${temp}.cmd
 
cd ../../

done