from gdown import download
from zipfile import ZipFile
import os
import tarfile
import sys


def main():
    link = sys.argv[1] if len(sys.argv) > 1 else None
    if link is None:
        print("Usage: python setup_cadence.py <google_drive_link>")
        sys.exit(1)
    
    download(link, "MSRF_General_Purpose_Plus.zip", fuzzy=True)
    with ZipFile("MSRF_General_Purpose_Plus.zip", 'r') as zip_ref: zip_ref.extractall(".")
    os.remove("MSRF_General_Purpose_Plus.zip")

    with tarfile.open("MSRF_General_Purpose_Plus/PDK/Cadence OA/tn65cmsp018k3_1_0c/PDK_CRN65GP_v1.0c_official_IC61_20101010_all.tar.gz", 'r') as tar_ref: tar_ref.extractall(".")

    os.mkdir("~/Documents/ASIC/TSMC-65nm")
    with tarfile.open("PDK_CRN65GP_v1.0c_official_IC61_20101010.tar.gz", 'r') as tar_ref: tar_ref.extractall("~/Documents/ASIC/TSMC-65nm/")

if __name__ == "__main__":
    main()