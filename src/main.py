import os

from copy_dir import copy_dir
from generate_page import generate_page

def main():
    src = os.path.abspath("static")
    dst = os.path.abspath("public")

    copy_dir(src, dst)

    generate_page("content/index.md", "template.html", "public/index.html")

main()