from pathlib import Path
from toolbox import Toolbox
from utils.argutils import print_args
from utils.modelutils import check_model_paths
import argparse
import torch
import os
import random
import numpy as np
import tensorflow as tf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Runs the toolbox",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-d", "--datasets_root", type=Path, help= \
        "Path to the directory containing your datasets. See toolbox/__init__.py for a list of "
        "supported datasets. You can add your own data by created a directory named UserAudio "
        "in your datasets root. Supported formats are mp3, flac, wav and m4a. Each speaker should "
        "be inside a directory, e.g. <datasets_root>/UserAudio/speaker_01/audio_01.wav.",
                        default=None)
    parser.add_argument("-e", "--enc_models_dir", type=Path, default="encoder/saved_models", 
                        help="Directory containing saved encoder models")
    parser.add_argument("-s", "--syn_models_dir", type=Path, default="synthesizer/saved_models", 
                        help="Directory containing saved synthesizer models")
    parser.add_argument("-v", "--voc_models_dir", type=Path, default="vocoder/saved_models", 
                        help="Directory containing saved vocoder models")
    parser.add_argument("--low_mem", action="store_true", help=\
        "If True, the memory used by the synthesizer will be freed after each use. Adds large "
        "overhead but allows to save some GPU memory for lower-end GPUs.")
    parser.add_argument("--reload_models", action="store_true", help=\
        "If True, reload synthesizer and vocoder models on each use for repeatable output.")
    parser.add_argument("--seed", type=int, default=None, help=\
        "Specifies a seed value for random number generation for deterministic behavior.")
    args = parser.parse_args()

    ## If "--reload_models" is specified, assign a default seed value if oneis not specified
    if args.reload_models and args.seed is None:
        args.seed = 0 

    print_args(args, parser)

    ## Initialize random number generators
    if args.seed:
        torch.manual_seed(args.seed)
        os.environ["PYTHONHASHSEED"] = str(args.seed)
        random.seed(args.seed)
        np.random.seed(args.seed)
        tf.compat.v1.set_random_seed(args.seed)

    ## Remind the user to download pretrained models if needed
    check_model_paths(encoder_path=args.enc_models_dir, synthesizer_path=args.syn_models_dir,
                      vocoder_path=args.voc_models_dir)

    # Launch the toolbox
    Toolbox(**vars(args))    
