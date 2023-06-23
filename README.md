> :construction: **Work in Progress** :construction:

# JPEG XL conformance bench

We compare how different implementations of [JPEG XL](https://jpegxl.info/) perform on the
[conformance tests](https://github.com/libjxl/conformance).

Currently we compare the following:

 - [libjxl](https://github.com/libjxl/libjxl), the reference implementation in C++
 - [libjxl](https://github.com/libjxl/libjxl) decoding to png
 - [jxl-oxide](https://github.com/tirr-c/jxl-oxide) a decoder written in pure Rust
 - [jxlatte](https://github.com/Traneptora/jxlatte) a pure java decoder


## How to generate a report

Some of the decoder are and the conformance tests are included as submodules, so as a first step after cloning this repo let's
```
git submodule update --recursive --init --depth 1 --recommend-shallow
 ```



### Building the decoders

#### libjxl
A simple way of building libjxl is
```bash
SKIP_TEST=1 ./third_party/libjxl/ci.sh opt
```
which should provide `./third_party/libjxl/build/tools/djxl`.

#### jxl-oxide
Make sure you have an up-to-date rust version, e.g. by running
```bash
rustup update
```

Then run
```bash
cargo install jxl-oxide-cli
```
which should provide the `jxl-dec` binary.

#### jxlatte
For building jxlatte, install `meson` and run
```bash
mkdir -p third_party/jxlatte/build
meson setup third_party/jxlatte/build third_party/jxlatte/
ninja -C third_party/jxlatte/build/
```
which should allow you to run `java -jar ./jxlatte/build/java/jxlatte.jar`.

### Running the conformance tests

#### Get conformance test data from Google Cloud bucket
First we need to get the actual test data for the conformance test, see instructions at
(https://github.com/libjxl/conformance) after installing gsutils, this boils down to
```bash
gcloud auth login
[follow instructions]
./third_party/conformance/scripts/download_and_symlink.sh
```

Then you can run the conformance test, let's say on the `main_level10` tests with all decoders, updating `./docs/dumps`, which are displayed by `docs/index.html`
```bash
./third_party/conformance/scripts/conformance.py --decoder "./third_party/libjxl/build/tools/djxl"  --corpus  ./third_party/conformance/testcases/main_level10.txt --results=./docs/dumps/dump_djxl.json
./third_party/conformance/scripts/conformance.py --decoder  "python3 scripts/wrap_png.py --decoder './third_party/libjxl/build/tools/djxl %s %s'"  --corpus  ./third_party/conformance/testcases/main_level10.txt --results=./docs/dumps/dump_djxl_via_png.json
./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder 'jxl-dec %s -o %s'"  --corpus  ./third_party/conformance/testcases/main_level10.txt --results=./docs/dumps/dump_jxl-dec.json
./third_party/conformance/scripts/conformance.py --decoder "python3 scripts/wrap_png.py --decoder 'java -jar ./third_party/jxlatte/build/java/jxlatte.jar %s %s'"  --corpus  ./third_party/conformance/testcases/main_level10.txt --results=./docs/dumps/dump_jxlatte.json
```
Alternative this can be done by running the [`update_dumps.sh`](./scripts/update_dumps.sh) script:
```bash
./scripts/update_dumps.sh ./third_party/conformance/testcases/main_level10.txt ./docs/dumps/

```
To see the report locally, you can then run
```
python3 -m http.server -d docs/
```
