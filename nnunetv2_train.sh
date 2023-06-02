#!/bin/bash
echo "Bash version ${BASH_VERSION}..."

# arg1 = task id
# arg2 = network (2d, 3d_fullres, 3d_lowres, 3d_cascade_fullres)
# Example: >>./nnunetv2_train.sh 110 2d

for (( i=0; i<=4; i++)) 
do
	nnUNetv2_train $1 $2 $i --npz
done
