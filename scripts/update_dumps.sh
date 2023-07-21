#!/bin/bash
set -x

# Test case corpus path
CORPUS=$1

# Results path
DUMP_PATH=$2

# Run conformance tests on all decoders
# djxl
python3 ./third_party/conformance/scripts/conformance.py --decoder "./third_party/libjxl/build/tools/djxl" --corpus $CORPUS --results=$DUMP_PATH/dump_djxl.json
# djxl via png
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder './third_party/libjxl/build/tools/djxl %s %s --bits_per_sample 16'" --corpus $CORPUS --results=$DUMP_PATH/dump_djxl_via_png.json --lax
# jxl-oxide
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder '/home/jon/.cargo/bin/jxl-dec %s -o %s -f png16'" --corpus $CORPUS --results=$DUMP_PATH/dump_jxl-dec.json --lax
# jxlatte
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder 'java -jar ./third_party/jxlatte/build/java/jxlatte.jar %s %s --png-depth=16'" --corpus $CORPUS --results=$DUMP_PATH/dump_jxlatte.json --lax
# j40
python3 ./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder './third_party/j40/dj40 %s %s'" --corpus $CORPUS --results=$DUMP_PATH/dump_j40.json --lax
