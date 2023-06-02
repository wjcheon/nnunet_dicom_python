Write-Host "PowerShell version $PSVersionTable.PSVersion..."

# arg1 = task id
# arg2 = network (2d, 3d_fullres, 3d_lowres, 3d_cascade_fullres)
# Example: >>./nnunetv2_train.ps1 110 2d


for ($i=0; $i -le 4; $i++)
{
    nnUNetv2_train $args[0] $args[1] $i --npz
}
