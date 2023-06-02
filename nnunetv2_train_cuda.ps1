Write-Host "PowerShell version $PSVersionTable.PSVersion..."

# arg[0] = task id
# arg[1] = network (2d, 3d_fullres, 3d_lowres, 3d_cascade_fullres)
# arg[2] = cuda id
# Example: >>./nnunetv2_train_cuda.ps1 011 2d 1
#CUDA_VISIBLE_DEVICES=$args[2] nnUNetv2_train $args[0] $args[1] $i --npz

$Env:CUDA_VISIBLE_DEVICES = $args[2]
for ($i=0; $i -le 4; $i++)
{
    nnUNetv2_train $args[0] $args[1] $i --npz --c
}
