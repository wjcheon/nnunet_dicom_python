import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import glob
from datetime import datetime
import re

folder_path = r"\\aria\NCC_Shared\NCC_AI\Liver\nas_ct_dcm_in"
local_nii_in = os.environ.get('local_nii_in')
local_nii_out = os.environ.get('local_nii_out')
nas_st_out = os.environ.get('nas_st_out')


class NewFolderEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            folder_name = os.path.basename(event.src_path)
            folder_full_path = os.path.join(folder_path, folder_name)
            print("DETECTION NEW FOLDER:", folder_full_path)

            time.sleep(10)
            start_time = time.time()
            # convert_to_nifti.py 스크립트 실행
            print("   DICOM2NII:Start - {}".format(folder_name))

            local_nii_in_temp = os.path.join(local_nii_in, folder_name)
            if not os.path.exists(local_nii_in_temp):
                os.makedirs(local_nii_in_temp)
            convert_script = "./convert_to_nifti.py"
            command = f"python {convert_script} \"{folder_full_path}\" \"{local_nii_in_temp}\""
            subprocess.run(command, shell=True)

            file_list = glob.glob(os.path.join(local_nii_in_temp, "*.nii.gz"))
            file_list.sort(key=os.path.getmtime, reverse=True)

            # Get the most recent file path
            most_recent_file = file_list[0] if file_list else None

            # 폴더 내 파일 개수로 세자리 숫자 생성
            file_count = len(file_list)+1
            padding_zeros = 3  # 세자리 숫자로 맞추기 위한 0 패딩 개수
            numeric_id = str(file_count).zfill(padding_zeros)

            # 현재 시간으로부터의 시간 문자열 생성
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")

            # 파일 이름 변경

            file_name = os.path.basename(most_recent_file)
            prefix, extension = os.path.splitext(file_name)
            extension_correct = ".nii.gz"
            new_file_name = f"LiTS_{numeric_id}_0000_{current_time}{extension_correct}"
            new_file_path = os.path.join(local_nii_in_temp, new_file_name)
            os.rename(most_recent_file, new_file_path)

            print('   DICOM2NII:Done - {}'.format(new_file_path))

            # Prediction
            print('   PREDICTION:Start - {}'.format(folder_name))
            prediction_script = "nnunetv2/inference/predict_liver.py"
            local_nii_out_temp = os.path.join(local_nii_out, folder_name)
            if not os.path.exists(local_nii_out_temp):
                os.makedirs(local_nii_out_temp)

            local_nii_out_filename = re.sub(r"(LiTS_\d+)_\d+_(\d+\.nii)", r"\1_\2", new_file_name)
            local_nii_out_fullfilename = os.path.join(local_nii_out_temp, local_nii_out_filename )
            command_predict = f"python {prediction_script} -i \"{new_file_path}\" -o \"{local_nii_out_fullfilename}\""
            subprocess.run(command_predict, shell=True)
            print('   PREDICTION:Done - {}'.format(folder_name))

            # Post-processing
            print('   POST-PROCESSING:Start - {}'.format(folder_name))
            postProcessing_script = "./post_process_segmentation.py"
            command_postProcessing = f"python {postProcessing_script} \"{local_nii_out_fullfilename}\" \"{local_nii_out_fullfilename}\""
            subprocess.run(command_postProcessing, shell=True)
            print('   POST-PROCESSING:DONE - {}'.format(folder_name))

            # Convert mask (nii) to dicom RT-structure
            print('   CONVERTING RT-STRUCTURE:Start - {}'.format(folder_name))
            convert_rtstructure_script = "./convert_to_RTSTRUCT.py"
            nas_rtst_out_temp = os.path.join(nas_st_out, folder_name)
            if not os.path.exists(nas_rtst_out_temp):
                os.makedirs(nas_rtst_out_temp)
            command_convertingRTstructure = f"python {convert_rtstructure_script} \"{local_nii_out_fullfilename}\" \"{folder_full_path}\" \"{nas_rtst_out_temp}\""
            subprocess.run(command_convertingRTstructure, shell=True)
            print('   CONVERTING RT-STRUCTURE:DONE - {}'.format(folder_name))


            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            print("Elapsed Time: {} minutes {} seconds".format(minutes, seconds))


            folder_paths_remove = [local_nii_in, local_nii_out]

            for folder_path_rm_temp in folder_paths_remove:
                for root, dirs, files in os.walk(folder_path_rm_temp, topdown=False):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        os.remove(file_path)
                    for dir_name in dirs:
                        dir_path = os.path.join(root, dir_name)
                        os.rmdir(dir_path)

                print("All files in", folder_path_rm_temp, "have been deleted.")



event_handler = NewFolderEventHandler()
observer = Observer()
observer.schedule(event_handler, folder_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()