from nnunetv2.paths import nnUNet_results, nnUNet_raw
import torch
from batchgenerators.utilities.file_and_folder_operations import join
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor

def main():
    # instantiate the nnUNetPredictor
    predictor = nnUNetPredictor(
        tile_step_size=0.5,
        use_gaussian=True,
        use_mirroring=True,
        perform_everything_on_gpu=True,
        device=torch.device('cuda', 0),
        verbose=False,
        verbose_preprocessing=False,
        allow_tqdm=True
    )
    # initializes the network architecture, loads the checkpoint
    # initialize_from_trained_model_folder(self,
    # model_training_output_dir: str,
    # use_folds: Union[Tuple[Union[int, str]], None],
    # checkpoint_name: str = 'checkpoint_final.pth'):

    predictor.initialize_from_trained_model_folder(
        join(nnUNet_results, 'Dataset770_LiTs2023', 'nnUNetTrainer__nnUNetPlans__3d_fullres'),
        use_folds=(0,),
        checkpoint_name='checkpoint_final.pth',
    )

    # variant 1: give input and output folders
    source_in = r'C:\Users\user\Desktop\in_liver'
    source_out =r'C:\Users\user\Desktop\out_liver'
    predictor.predict_from_files(source_in,
                                 source_out,
                                 save_probabilities=False, overwrite=False,
                                 num_processes_preprocessing=2, num_processes_segmentation_export=2,
                                 folder_with_segs_from_prev_stage=None, num_parts=1, part_id=0)


if __name__ == "__main__":
    main()