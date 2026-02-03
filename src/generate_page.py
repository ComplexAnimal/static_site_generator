import os

from md_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_pages_recursive(from_path, temp_path, dest_path):

    with temp_path.open("r", encoding="utf-8") as f:
        template = f.read()

    for item in from_path.iterdir():
        relative = item.relative_to(from_path)
        dest = dest_path / relative

        if item.is_file():
            html_dest = dest.with_suffix(".html")

            with item.open("r", encoding="utf-8") as f:
                markdown = f.read()

            node = markdown_to_html_node(markdown)
            html = node.to_html()
            title = extract_title(markdown)
            page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
            html_dest.parent.mkdir(parents=True, exist_ok=True)

            with html_dest.open("w", encoding="utf-8") as f:
                f.write(page)

        else:
            generate_pages_recursive(item, temp_path, dest)