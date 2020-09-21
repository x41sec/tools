#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Function: decompress special Xamarin .dll files"""

"""
Background information and file format documentation:
https://github.com/xamarin/xamarin-android/pull/4686

Installation notes:
This program requires the python lz4 library.
Install via 
* "lz4" (pip) 
* "python3-lz4" (Debian, Ubuntu)


MIT License

Copyright (c) 2020 Christian Reitter, X41 D-Sec GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import lz4.block
import sys
import struct

def print_usage_and_exit(): 
    sys.exit("usage: ./command compressed-inputfile.dll uncompressed-outputfile.dll")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage_and_exit()

    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    header_expected_magic = b'XALZ'
    
    with open(input_filepath, "rb") as xalz_file:
        data = xalz_file.read()
    
        if data[:4] != header_expected_magic:
            sys.exit("The input file does not contain the expected magic bytes, aborting ...")
    
        header_index = data[4:8]
        header_uncompressed_length = struct.unpack('<I', data[8:12])[0]
        payload = data[12:]
        
        print("header index: %s" % header_index)
        print("compressed payload size: %s bytes" % len(payload))
        print("uncompressed length according to header: %s bytes" % header_uncompressed_length)
        
        decompressed = lz4.block.decompress(payload, uncompressed_size=header_uncompressed_length)
                
        with open(output_filepath, "wb") as output_file:
            output_file.write(decompressed)
            output_file.close()
        print("result written to file")
