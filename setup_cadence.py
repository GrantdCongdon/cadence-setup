from gdown import download
from zipfile import ZipFile
import os
import tarfile
import sys
import shutil


def main():
    link = sys.argv[1] if len(sys.argv) > 1 else None
    if link is None:
        print("Usage: python setup_cadence.py <google_drive_link>")
        sys.exit(1)
    
    download(link, "MSRF_General_Purpose_Plus.zip", fuzzy=True)
    with ZipFile("MSRF_General_Purpose_Plus.zip", 'r') as zip_ref: zip_ref.extractall(".")

    os.mkdir("temp")
    with tarfile.open("MSRF_General_Purpose_Plus/PDK/Cadence OA/tn65cmsp018k3_1_0c/PDK_CRN65GP_v1.0c_official_IC61_20101010_all.tar.gz", 'r') as tar_ref: tar_ref.extractall("./temp/", filter='data')

    home_dir = os.path.expanduser("~")
    os.mkdir(f"{home_dir}/Documents/ASIC")
    os.mkdir(f"{home_dir}/Documents/ASIC/TSMC-65nm")
    with tarfile.open("temp/PDK_CRN65GP_v1.0c_official_IC61_20101010.tar.gz", 'r') as tar_ref: tar_ref.extractall(f"{home_dir}/Documents/ASIC/TSMC-65nm/", filter='data')

    shutil.rmtree("temp")
    shutil.rmtree("MSRF_General_Purpose_Plus")
    os.remove("MSRF_General_Purpose_Plus.zip")

    os.chdir(f"{home_dir}/Documents/ASIC/TSMC-65nm/")
    os.system("./pdkInstall.pl <<< $'3\n1\n3\n2\ny\n'")

    with open("lib.defs", "w") as f:
        f.write(f"DEFINE tsmcN65 {home_dir}/Documents/ASIC/TSMC-65nm/tsmcN65\n")
        f.write("ASSIGN tsmcN65 libMode shared\n")

    os.chdir(home_dir)
    with open("cds.lib", "w") as f:
        f.write("SOFTINCLUDE /package/eda/cadence/IC231.060/share/cdssetup/cds.lib\n")
        f.write(f"INCLUDE {home_dir}/Documents/ASIC/TSMC-65nm/lib.defs\n")

    os.system("module load cadence/virtuoso")
    os.system("module load cadence/spectre")
    os.system("module load keysight/ads")
    os.system("module load cadence/virtuoso-advanced")
    os.system("module save ASIC")

    with open(".setup_cadence.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\nmodule restore ASIC\n")
        f.write("\nexport OA_HOME=/package/eda/cadence/IC231.060/oa_v22.61.013\n")
        f.write(f"\nexport CDS_LIB_PATH={home_dir}/Documents/ASIC/TSMC-65nm/libs.defs\n")
        f.write("\nexport PATH=/package/eda/cadence/IC231.060/tools/dfII/bin:$PATH\n")

    os.system("chmod +x .setup_cadence.sh")
    os.system("source .setup_cadence.sh")

    shutil.rmtree("cadence-setup")

    return

if __name__ == "__main__":
    main()