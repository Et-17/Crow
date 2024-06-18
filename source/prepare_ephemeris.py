# This file downloads the ephemeris file from the JPL Development Ephemeris if
# it hasn't been already, and then converts it to the custom format for use by
# the C code.

# Description of custom ephemeris format:
# struct block {
#     float start;
#     float end;
#     float sun[13][3][2];
#     float moon[13][3][8];
# };

import os
from urllib.request import urlretrieve
import math
import struct
import sys

# You can pass two arguments, the start of the generated ephemeris and the end.
# If you just pass one number, it will be assumed to be the start and it will
# generate until the end of the input. If you don't give any, it will default to
# all of the input.

EPHEMERIS_START = -math.inf
EPHEMERIS_END = math.inf

if len(sys.argv) == 2:
    EPHEMERIS_START = float(sys.argv[1])
elif len(sys.argv) == 3:
    EPHEMERIS_START = float(sys.argv[1])
    EPHEMERIS_END = float(sys.argv[2])

OUTPUT_FILE_PATH = os.path.join(os.getcwd(), "ephemeris")

EPHEMERIS_FILE_PATH = os.path.join(os.getcwd(), "ascp01950.440")
EPHEMERIS_FILE_WEB_ADDRESS = "https://ssd.jpl.nasa.gov/ftp/eph/planets/ascii/de440/ascp01950.440"

def install_ephemeris():
    if not os.path.exists(EPHEMERIS_FILE_PATH):
        print("Ephemeris file not found, redownloading")
        urlretrieve(EPHEMERIS_FILE_WEB_ADDRESS, EPHEMERIS_FILE_PATH)
        print("Downloaded ephemeris file")
    else:
        print("Ephemeris already downloaded")


LUNAR_COEFF_START = 440
SOLAR_COEFF_START = 230
COMPONENTS = 3
COEFFS = 13
LUNAR_SUBDIVS = 8
SOLAR_SUBDIVS = 2

def extract_subdiv(start, subdiv, block):
    subdiv_start_index = start + subdiv * COEFFS * COMPONENTS
    x = block[subdiv_start_index : subdiv_start_index + COEFFS]
    y = block[subdiv_start_index + COEFFS : subdiv_start_index + COEFFS * 2]
    z = block[subdiv_start_index + COEFFS * 2 : subdiv_start_index + COEFFS * 3]
    return x + y + z

# takes in a raw block from the ephemeris file, and returns a block struct
def process_block(block):
    processed_struct = []
    processed_struct.append(block[0]) # start time
    processed_struct.append(block[1]) # end time
    for subdiv in range(SOLAR_SUBDIVS):
        processed_struct.extend(extract_subdiv(SOLAR_COEFF_START, subdiv, block))
    for subdiv in range(LUNAR_SUBDIVS):
        processed_struct.extend(extract_subdiv(LUNAR_COEFF_START, subdiv, block))
    return processed_struct

BYTES_PER_GROUP = 26820
GROUPS_PER_FILE = 1142

def process_blocks():
    ephemeris_file = open(EPHEMERIS_FILE_PATH, "r")
    output_file = open(OUTPUT_FILE_PATH, "wb")
    for group_num in range(GROUPS_PER_FILE):
        lines = ephemeris_file.readlines(BYTES_PER_GROUP)[1:]
        block = []
        for line in lines:
            for num in line.split():
                block.append(float(num.replace("D", "e")))
        # check if block is within date range
        if not ((block[0] <= EPHEMERIS_END) and (block[1] >= EPHEMERIS_START)):
            continue
        processed = process_block(block)
        for num in processed:
            output_file.write(struct.pack("@f", num))

def setup():
    print("Checking ephemeris file")
    install_ephemeris()
    print("Processing blocks")
    process_blocks()
    print("Done")

if __name__ == "__main__":
    setup()
