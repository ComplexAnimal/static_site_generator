import os

from md_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, basepath):

    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:
        template = file.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Update to make basepath customizable
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, "w")
    f.write(page)
    f.close()

def generate_pages_recursive(from_path, temp_path, dest_path, basepath):

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

            # Update to make basepath customizable
            page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

            html_dest.parent.mkdir(parents=True, exist_ok=True)

            with html_dest.open("w", encoding="utf-8") as f:
                f.write(page)

        else:
            generate_pages_recursive(item, temp_path, dest, basepath)