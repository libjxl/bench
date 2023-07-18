#!/usr/bin/env python3
import sys
import numpy as np
import subprocess
import tempfile
import argparse
import shlex
import json
import os

from apng import APNG, make_text_chunk
import png

def convert_to_png(temp_file, args):
    subprocess.run(shlex.split(args.decoder_format % (args.input, temp_file.name)), check=True)

def convert_to_numpy_array(temp_file, args):
    img = APNG.open(temp_file);
    frames = []
    for frame, control in img.frames:
        reader = png.Reader(bytes=frame.to_bytes())
        width,height,rows,info = reader.asDirect()
        print(info)
        nbchans = info['planes']
        frame = np.vstack([s for s in map(np.uint16, [np.asarray(row) for row in rows])])
        frame = np.reshape(frame, (height, width, info['planes']))
        frame_array = np.array(frame).astype(np.float64) / (2**info['bitdepth'] - 1)
        frames.append(frame_array)

    img_array = np.stack(frames)
    print(args.output)
    np.save(args.output, img_array)
    return nbchans


def write_metadata(args):
    with open(args.metadata_out, 'w') as f:
        json.dump({"frames": [ { "name": "", } ], }, f)

# Skip for now
def write_orig_icc(args):
    return

# Placeholder: let ImageMagick extract an icc profile from the PNG and assume it otherwise is sRGB or gray with the sRGB transfer curve
# TODO(jon): make this also work for PNG files that use other ways to signal their colorspace
def write_icc(temp_file, args, nbchans):
    subprocess.run(["convert", temp_file.name, args.icc_out])
    if (os.path.getsize(args.icc_out) == 0):
        if nbchans >= 3:
            with open('scripts/sRGB.icc', 'rb') as file:
                binary_data = file.read()
        else:
            with open('scripts/sRGB-Gray.icc', 'rb') as file:
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
        nbchans = convert_to_numpy_array(temp_file, args)
        write_icc(temp_file, args, nbchans)
    write_metadata(args)
    write_orig_icc(args)

if __name__ == "__main__":
    main()
