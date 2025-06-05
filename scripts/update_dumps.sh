#!/bin/bash
set -x

# Create a new virtual environment.
python3 -m venv .venv

# Activate the virtual environment.
source .venv/bin/activate

# Ensure the virtual environment is deactivated on exit.
trap deactivate EXIT

# Install the needed packages in the virtual environment.
pip install pypng numpy apng


# Test case corpus path
CORPUS=$1

# Results path
DUMP_PATH=$2

# Run conformance tests on all decoders
# djxl
python3 ./third_party/conformance/scripts/conformance.py --decoder "./third_party/libjxl/build/tools/djxl" --corpus $CORPUS --results=$DUMP_PATH/dump_djxl.json --lax
# djxl via png
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder './third_party/libjxl/build/tools/djxl %s %s --bits_per_sample 16'" --corpus $CORPUS --results=$DUMP_PATH/dump_djxl_via_png.json --lax
# jxl-rs
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_jxl-rs.py --decoder ' third_party/jxl-rs/target/release/jxl_cli %s %s --icc-out %s'" --corpus $CORPUS --results=$DUMP_PATH/dump_jxl-rs.json --lax
# jxl-rs via png
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder ' third_party/jxl-rs/target/release/jxl_cli %s %s '" --corpus $CORPUS --results=$DUMP_PATH/dump_jxl-rs_via_png.json --lax
# jxl-oxide
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_jxl_oxide.py --decoder 'jxl-oxide %s --icc-output %s -o %s -f npy'" --corpus $CORPUS --results=$DUMP_PATH/dump_jxl-oxide.json --lax
# jxlatte
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder 'java -jar ./third_party/jxlatte/build/java/jxlatte.jar %s %s --png-depth=16'" --corpus $CORPUS --results=$DUMP_PATH/dump_jxlatte.json --lax
# j40
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder './third_party/j40/dj40 %s %s'" --corpus $CORPUS --results=$DUMP_PATH/dump_j40.json --lax
