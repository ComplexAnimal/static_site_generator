import os

from md_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):

    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:
        template = file.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, "w")
    f.write(page)
    f.close()