import os
import shutil

def main():
    src = os.path.abspath("static")
    dst = os.path.abspath("public")
    copy_dir(src, dst)

def copy_dir(src, dst):
    # Check for source and destination directories:
    if not os.path.exists(src):
        raise Exception("Error: source directory missing")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    # Copy src contents to dst:
    contents = os.listdir(src)
    for item in contents:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            # Recursively call copy_dir(src_path, dst_path)
            copy_dir(src_path, dst_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line[:2] == "# ":
            title = line[2:].strip()
            break
    if not title:
        raise Exception("Error: No h1 heading")
    else:
        return title

main()