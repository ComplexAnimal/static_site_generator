import os
from pathlib import Path

from copy_dir import copy_dir
from generate_page import generate_pages_recursive

def main():
    src = os.path.abspath("static")
    dst = os.path.abspath("public")
    copy_dir(src, dst)

    from_path = Path("content")
    temp_path = Path("template.html")
    dest_path = Path("public")
    generate_pages_recursive(from_path, temp_path, dest_path)

main()