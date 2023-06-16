#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image
from PIL import ImageSequence
import subprocess
import tempfile
import argparse
import shlex
import json


def convert_to_png(temp_file, args):
    subprocess.run(shlex.split(args.decoder) + [args.input, temp_file.name], check=True)

def convert_to_numpy_array(temp_file, args):
    img = Image.open(temp_file.name)
    frames = []

    for frame in ImageSequence.Iterator(img):
        frame_array = np.array(frame).astype(np.float64) / 255.0
        frames.append(frame_array)

    img_array = np.stack(frames)
    print(args.output)
    np.save(args.output, img_array)


def write_metadata(args):
    with open(args.metadata_out, 'w') as f:
        json.dump({"frames": [ { "name": "", } ], }, f)

def write_orig_icc(args):
    with open(args.orig_icc_out, 'w') as f:
        pass

def write_icc(args):
    with open(args.icc_out, 'w') as f:
        pass

def write_reconstruct_jpg(args):
    with open(args.output, 'w') as f:
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',
                        metavar='INPUT',
                        help='path to the input .jxl file')
    parser.add_argument('output',
                        metavar='OUTPUT',
                        help='path to the output .npy file')
    parser.add_argument('--decoder',
                        metavar='DECODER',
                        required=True,
                        help='path to the decoder binary assuming [decoder] in.jxl out.png syntax')
    parser.add_argument('--orig_icc_out',
                        metavar='ORIG_ICC_OUT',
                        help='path to the original ICC output')
    parser.add_argument('--metadata_out',
                        metavar='METADATA_OUT',
                        help='path to the metadata output')
    parser.add_argument('--icc_out',
                        metavar='ICC_OUT',
                        help='path to the ICC output')
    parser.add_argument('--norender_spotcolors',
                        action='store_true',
                        help='flag to disable rendering of spot colors')

    args = parser.parse_args()

    if args.output.endswith('.jpg'):
        write_reconstruct_jpg(args)
        return

    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
        convert_to_png(temp_file, args)
        convert_to_numpy_array(temp_file, args)
    write_metadata(args)
    write_orig_icc(args)
    write_icc(args)

if __name__ == "__main__":
    main()
