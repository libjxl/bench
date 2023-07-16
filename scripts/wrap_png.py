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
import os


def convert_to_png(temp_file, args):
    subprocess.run(shlex.split(args.decoder_format % (args.input, temp_file.name)), check=True)

def convert_to_numpy_array(temp_file, args):
    img = Image.open(temp_file.name)
    frames = []

    for frame in ImageSequence.Iterator(img):
        if len(np.shape(frame)) == 2:
            frame = np.reshape(frame,np.shape(frame) + (1,))
        frame_array = np.array(frame).astype(np.float64) / 255.0
        frames.append(frame_array)

    img_array = np.stack(frames)
    print(args.output)
    np.save(args.output, img_array)


def write_metadata(args):
    with open(args.metadata_out, 'w') as f:
        json.dump({"frames": [ { "name": "", } ], }, f)

# Skip for now
def write_orig_icc(args):
    return

# Placeholder: let ImageMagick extract an icc profile from the PNG and assume it otherwise is sRGB
# TODO(jon): make this also work for PNG files that use other ways to signal their colorspace
def write_icc(temp_file, args):
    subprocess.run(["convert", temp_file.name, args.icc_out])
    if (os.path.getsize(args.icc_out) == 0):
        with open('scripts/sRGB.icc', 'rb') as file:
            binary_data = file.read()
        with open(args.icc_out, 'wb') as file:
            file.write(binary_data)


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
    parser.add_argument('--decoder_format',
                        metavar='DECODER',
                        required=True,
                        help='path to the decoder binary assuming that the two  syntax')
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
    parser.add_argument('--output_flag',
                        metavar='OUTPUT_FLAG',
                        help='the name of hte flag used by the decoder to communicate the output file')

    args = parser.parse_args()

    if args.output.endswith('.jpg'):
        write_reconstruct_jpg(args)
        return

    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
        convert_to_png(temp_file, args)
        write_icc(temp_file, args)
        convert_to_numpy_array(temp_file, args)
    write_metadata(args)
    write_orig_icc(args)

if __name__ == "__main__":
    main()
