import os
import shutil

from copy_dir import copy_dir

def main():
    src = os.path.abspath("static")
    dst = os.path.abspath("public")

    copy_dir(src, dst)

main()