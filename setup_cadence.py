from gdown import download
from zipfile import ZipFile
from os import mkdir, chdir, remove, path, system
from sys import argv, exit
from shutil import rmtree
import tarfile

def main():
    link = argv[1] if len(argv) > 1 else None
    if link is None:
        print("Usage: python setup_cadence.py <google_drive_link>")
        exit(1)

    home_dir = path.expanduser("~")
    asic_dir = f"{home_dir}/Documents/ASIC"

    # (GDrive Download)
    download(link, "MSRF_General_Purpose_Plus.zip", fuzzy=True)

    # Extract only the PDK file version we need to avoid hitting disk quota
    with ZipFile("MSRF_General_Purpose_Plus.zip", 'r') as zip_ref: zip_ref.extract("MSRF_General_Purpose_Plus/PDK/Cadence OA/tn65cmsp018k3_1_0c/PDK_CRN65GP_v1.0c_official_IC61_20101010_all.tar.gz")

    # Delete the original drive download earlier to avoid hitting disk quota
    remove("MSRF_General_Purpose_Plus.zip")

    mkdir("temp")
    with tarfile.open("MSRF_General_Purpose_Plus/PDK/Cadence OA/tn65cmsp018k3_1_0c/PDK_CRN65GP_v1.0c_official_IC61_20101010_all.tar.gz", 'r') as tar_ref: tar_ref.extractall("./temp/", filter='data')

    # Delete the tar.gz file above earlier to avoid hitting disk quota
    rmtree("MSRF_General_Purpose_Plus")

    # Make ASIC directory
    mkdir(f"{asic_dir}")
    mkdir(f"{asic_dir}/TSMC-65nm")
    with tarfile.open("temp/PDK_CRN65GP_v1.0c_official_IC61_20101010.tar.gz", 'r') as tar_ref: tar_ref.extractall(f"{asic_dir}/TSMC-65nm/", filter='data')

    rmtree("temp")

    chdir(f"{asic_dir}/TSMC-65nm/")
    system("./pdkInstall.pl <<< $'3\n1\n3\n2\ny\n'")

    with open("lib.defs", "w") as f:
        f.write(f"DEFINE tsmcN65 {asic_dir}/TSMC-65nm/tsmcN65\n")
        f.write("ASSIGN tsmcN65 libMode shared\n")

    chdir(home_dir)
    with open("cds.lib", "w") as f:
        f.write("SOFTINCLUDE /package/eda/cadence/IC231.060/share/cdssetup/cds.lib\n")
        f.write(f"INCLUDE {asic_dir}/TSMC-65nm/lib.defs\n")

    with open(".setup_cadence.sh", "w") as f:
        f.write("#!/bin/bash\n")
        # Because thinlinc hates us (forces us to use r*d h*t ent*rpr*se linux)
        f.write("export LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH:/package/eda/cadence/ICADVM201.34/tools.lnx86/lib/64bit/RHEL/RHEL8/\n\"")
        f.write("module restore ASIC\n")
        f.write("\nexport OA_HOME=/package/eda/cadence/IC231.060/oa_v22.61.013\n")
        f.write(f"export CDS_LIB_PATH={home_dir}/Documents/ASIC/TSMC-65nm/libs.defs\n")
        f.write("export PATH=/package/eda/cadence/IC231.060/tools/dfII/bin:$PATH\n")

    system("chmod +x .setup_cadence.sh")

    return

if __name__ == "__main__":
    main()
