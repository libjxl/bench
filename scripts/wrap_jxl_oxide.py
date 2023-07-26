#!/usr/bin/env python3
import sys
import subprocess
import argparse
import shlex
import json
import os

def write_metadata(args):
    with open(args.metadata_out, 'w') as f:
        json.dump({"frames": [ { "name": "", } ], }, f)

# Skip for now
def write_orig_icc(args):
    return


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
                        help='path to the decoder binary assuming that the three %s syntax')
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

    subprocess.run(shlex.split(args.decoder_format % (args.input, args.icc_out, args.output)), check=True)
    write_metadata(args)
    write_orig_icc(args)

if __name__ == "__main__":
    main()
