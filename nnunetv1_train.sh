#!/bin/bash
echo "Bash version ${BASH_VERSION}..."

# arg1 = network (2d, 3d_fullres, 3d_lowres, 3d_cascade_fullres)
# arg2 = network_trainer (nnUNetTrainerV2: default)
# arg3 = task id
# Example: >>./myscript.sh 2d nnUNetTrainerV2 100

for (( i=0; i<=4; i++)) 
do
	nnUNet_train $1 $2 $3 $i --npz
done
