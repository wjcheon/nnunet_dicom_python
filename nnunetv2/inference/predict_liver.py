from nnunetv2.paths import nnUNet_results, nnUNet_raw
import torch
from batchgenerators.utilities.file_and_folder_operations import join
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import os
import argparse


def get_parser():
    """
    Parse input arguments.
    """
    parser = argparse.ArgumentParser(description='Perform Auto-segmentation (nii2nii)')

    # Positional arguments.
    parser.add_argument("-i", help="Path to input NIFTI images")
    parser.add_argument("-o", help="Path to output NIFTI image")
    return parser.parse_args()


def main(input_path, output_path):
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

        # variant 2, use list of files as inputs. Note how we use nested lists!!!
    indir, input_filename = os.path.split(input_path)
    outdir, output_filename = os.path.split(output_path)

    predictor.predict_from_files([[join(indir, input_filename)]],
                                 [join(outdir, output_filename)],
                                 save_probabilities=False, overwrite=True,
                                 num_processes_preprocessing=2, num_processes_segmentation_export=2,
                                 folder_with_segs_from_prev_stage=None, num_parts=1, part_id=0)


if __name__ == "__main__":
    p = get_parser()
    main(p.i, p.o)
