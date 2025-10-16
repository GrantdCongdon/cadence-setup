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

    os.mkdir("temp")
    with tarfile.open("MSRF_General_Purpose_Plus/PDK/Cadence OA/tn65cmsp018k3_1_0c/PDK_CRN65GP_v1.0c_official_IC61_20101010_all.tar.gz", 'r') as tar_ref: tar_ref.extractall("./temp/")

    os.mkdir("~/Documents/ASIC")
    os.mkdir("~/Documents/ASIC/TSMC-65nm")
    with tarfile.open("temp/PDK_CRN65GP_v1.0c_official_IC61_20101010.tar.gz", 'r') as tar_ref: tar_ref.extractall("~/Documents/ASIC/TSMC-65nm/")

    os.remove("temp", recursive=True)
    os.remove("MSRF_General_Purpose_Plus", recursive=True)
    os.remove("MSRF_General_Purpose_Plus.zip")

    os.chdir("~/Documents/ASIC/TSMC-65nm/")
    # execute a pearl script but include injection of the numbers "3," "1," "3," "2" but when prompted for input
    os.system("./pdkInstall.pl <<< $'3\n1\n3\n2\n'")
if __name__ == "__main__":
    main()