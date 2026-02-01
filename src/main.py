import os
import shutil
from pathlib import Path

from md_to_html import markdown_to_html_node

def main():
    # Copy static dir to public dir
    src = os.path.abspath("static")
    dst = os.path.abspath("public")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    copy_dir(src, dst)

    content_dir = Path("content")

    for md_path in content_dir.rglob("*.md"):
        relative = md_path.relative_to(content_dir)
        relative_html = relative.with_suffix(".html")
        dest_path = Path("public") / relative_html
        generate_page(str(md_path), "template.html", str(dest_path))

def copy_dir(src, dst):
    if not os.path.exists(dst):
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

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path) as file:
        md_text = file.read()

    with open(template_path) as file:
        page = file.read()

    title = extract_title(md_text)
    node = markdown_to_html_node(md_text)
    html = node.to_html()

    page = page.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, "w")
    f.write(page)
    f.close()

main()