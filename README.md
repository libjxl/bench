# JPEG XL conformance bench

We compare how different implementations of [JPEG XL](https://jpegxl.info/) perform on the
[conformance tests](https://github.com/libjxl/conformance).

Currently we compare the following:

 - [libjxl](https://github.com/libjxl/libjxl), the reference implementation in C++
 - [libjxl](https://github.com/libjxl/libjxl) decoding to png
 - [jxl-oxide](https://github.com/tirr-c/jxl-oxide) a decoder written in pure Rust
 - [jxlatte](https://github.com/Traneptora/jxlatte) a pure java decoder


## How to generate a report



### Building the decoders



### jxl-oxide
For jxl-oxide, we run
```
cargo install jxl-oxide-cli
```
which should provdide the `jxl-dec` binary.


