import os
from urllib.request import urlretrieve
import math
import datetime

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
COMPONENTS = 3
COEFFS = 13
SUBDIVS = 8

def process_block(block):
    start_time = block[0]
    end_time = block[1]
    block_subdivisions = []
    for subdiv in range(SUBDIVS):
        current_subdiv_start_index = LUNAR_COEFF_START + subdiv * COEFFS * COMPONENTS
        current_subdiv_coeffs = [
            block[current_subdiv_start_index : current_subdiv_start_index + COEFFS],
            block[current_subdiv_start_index + COEFFS : current_subdiv_start_index + COEFFS * 2],
            block[current_subdiv_start_index + COEFFS * 2 : current_subdiv_start_index + COEFFS * 3]
        ]
        current_subdiv_start = start_time + ((end_time - start_time) / SUBDIVS * subdiv)
        current_subdiv_end = start_time + ((end_time - start_time) / SUBDIVS * (subdiv+1))
        block_subdivisions.append((current_subdiv_start, current_subdiv_end, current_subdiv_coeffs))
    return block_subdivisions


BYTES_PER_GROUP = 26820
GROUPS_PER_FILE = 1142

def process_blocks():
    ephemeris_file = open(EPHEMERIS_FILE_PATH, "r")
    raw_blocks = []
    for group_num in range(GROUPS_PER_FILE):
        lines = ephemeris_file.readlines(BYTES_PER_GROUP)[1:]
        block = []
        for line in lines:
            for num in line.split():
                block.append(float(num.replace("D", "e")))
        raw_blocks.append(process_block(block))
    return raw_blocks

def flatten_extraction(extraction):
    subdivisions = {}
    for block in extraction:
        for subdivision in block:
            subdivisions[subdivision[:2]] = subdivision[2]
    return subdivisions

def setup():
    print("Checking ephemeris file")
    install_ephemeris()
    print("Processing blocks")
    extraction = process_blocks()
    print("Flattening extraction")
    extraction = flatten_extraction(extraction)
    print("Done")
    return extraction
