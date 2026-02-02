import os
import shutil

def copy_dir(src, dst, is_root=True):

    if is_root and os.path.exists(dst):
        shutil.rmtree(dst)

    if not os.path.exists(dst):
        os.mkdir(dst)
        print(f'Created directory: {dst}')

    for item in os.listdir(src):

        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f'Copied file: {item}')

        else:
            copy_dir(src_path, dst_path, is_root=False)