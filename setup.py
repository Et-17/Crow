import os
from urllib.request import urlretrieve

ephemeris_file_path = os.path.join(os.getcwd(), "ascp01950.440")
ephemeris_file_web_address = "https://ssd.jpl.nasa.gov/ftp/eph/planets/ascii/de440/ascp01950.440"

def install_ephemeris():
    if not os.path.exists(ephemeris_file_path):
        print("Ephemeris file not found, redownloading")
        urlretrieve(ephemeris_file_web_address, ephemeris_file_path)
        print("Downloaded ephemeris file")
    else:
        print("Ephemeris already downloaded")

install_ephemeris()
