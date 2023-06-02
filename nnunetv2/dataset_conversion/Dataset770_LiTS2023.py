from batchgenerators.utilities.file_and_folder_operations import *
import shutil
from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw
import os
import re
import nibabel as nib
from tqdm import tqdm

def convert_lits2023(lits_base_dir: str, nnunet_dataset_id: int = 770):
    task_name = "LiTs2023"

    foldernameNew = "Dataset%03.0d_%s" % (nnunet_dataset_id, task_name)
    folderPath = "D:\Reaserch DB\3_Segmentation\LiTs"
    # setting up nnU-Net folders
    out_base = join(nnUNet_raw, foldernameNew)
    imagestr = join(out_base, "imagesTr")
    labelstr = join(out_base, "labelsTr")
    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(labelstr)

    lits_ct_base_dir = os.path.join(lits_base_dir, 'CT_Vol', 'CT_Vol')
    lits_label_base_dir = os.path.join(lits_base_dir, 'CT_Mask', 'CT_Mask')
    file_list_ct = os.listdir(lits_ct_base_dir)
    file_list_label = os.listdir(lits_label_base_dir)


    segmentation_pattern = r'segmentation-(\d+)\.nii$'
    volume_pattern = r'volume-(\d+)\.nii$'

    if len(file_list_ct) != len(file_list_label):
        print("Error: Number of segmentation files and volume files do not match!")
    else:
        progress_bar = tqdm(enumerate(file_list_label), total=len(file_list_label), desc="Renaming Files")
        for i, segmentation_file in progress_bar:
        #for i, segmentation_file in enumerate(file_list_label):
            if segmentation_file.startswith('segmentation-') and segmentation_file.endswith('.nii'):
                segmentation_match = re.match(segmentation_pattern, segmentation_file)
                if segmentation_match:
                    segmentation_number = int(segmentation_match.group(1))
                    volume_match = [file for file in file_list_ct if re.match(volume_pattern, file) and int(
                        re.match(volume_pattern, file).group(1)) == segmentation_number]
                    if volume_match:
                        volume_file = volume_match[0]

                        ct_new_file_name = 'LiTS_{:03d}_0000.nii.gz'.format(i)
                        label_new_file_name = 'LiTS_{:03d}.nii.gz'.format(i)

                        new_ct_path = os.path.join(imagestr, ct_new_file_name)
                        new_label_path = os.path.join(labelstr, label_new_file_name)

                        ct_source_path = os.path.join(lits_ct_base_dir, volume_match[0])
                        ct_target_path = new_ct_path

                        label_source_path = os.path.join(lits_label_base_dir, segmentation_file)
                        label_target_path = new_label_path

                        # 파일 읽기
                        img = nib.load(ct_source_path)
                        label = nib.load(label_source_path)

                        # 파일 저장
                        nib.save(img, ct_target_path)
                        nib.save(label, label_target_path)

                        # 원본 파일 삭제 (선택 사항)
                        #os.remove(source_path)

                        print('Renamed:', volume_match[0], 'to', label_new_file_name)
                        print('Renamed:', segmentation_file, 'to', ct_new_file_name)

                    else:
                        print('Error: Corresponding volume file not found for segmentation file:', segmentation_file)
                else:
                    print('Error: File name format is incorrect:', segmentation_file)

        print("File renaming completed successfully.")

    # generate_dataset_json(out_base, {0: "CT"},
    #                       labels={
    #                           "background": 0,
    #                           "kidney": (1, 2, 3),
    #                           "masses": (2, 3),
    #                           "tumor": 2
    #                       },
    #                       regions_class_order=(1, 3, 2),
    #                       num_training_cases=len(cases), file_ending='.nii.gz',
    #                       dataset_name=task_name, reference='none',
    #                       release='prerelease',
    #                       overwrite_image_reader_writer='NibabelIOWithReorient',
    #                       description="KiTS2023")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str,
                        help="The downloaded and extracted KiTS2023 dataset (must have case_XXXXX subfolders)")
    parser.add_argument('-d', required=False, type=int, default=770, help='nnU-Net Dataset ID, default: 770')
    args = parser.parse_args()
    amos_base = args.i
    convert_lits2023(amos_base, args.d)

    # /media/isensee/raw_data/raw_datasets/kits23/dataset

