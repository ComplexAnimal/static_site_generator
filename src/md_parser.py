import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) < 3 or len(split_nodes) % 2 == 0:
                raise Exception("Error: The text is missing a closing delimiter")
            else:
                node_group = []
                for i in range(len(split_nodes)):
                    if i % 2 == 0: # Should always be plain text
                        if split_nodes[i] != "":
                            new_node = TextNode(split_nodes[i], TextType.TEXT)
                            node_group.append(new_node)
                    else: # For all other text types
                        new_node = TextNode(split_nodes[i], text_type)
                        node_group.append(new_node)
                new_nodes.extend(node_group)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            remaining = node.text
            for i in range(len(images)):
                image_alt, image_link = images[i]
                delimiter = f"![{image_alt}]({image_link})"
                sections = remaining.split(delimiter, 1)
                current = sections[0]
                remaining = sections[1]
                if current != "":
                    new_nodes.append(TextNode(current, TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAG, image_link))
                if i == len(images) - 1 and remaining != "":
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            remaining = node.text
            for i in range(len(links)):
                anchor_text, url = links[i]
                delimiter = f"[{anchor_text}]({url})"
                sections = remaining.split(delimiter, 1)
                current = sections[0]
                remaining = sections[1]
                if current != "":
                    new_nodes.append(TextNode(current, TextType.TEXT))
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                if i == len(links) - 1 and remaining != "":
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def text_to_text_nodes(text):
    root_node = TextNode(text, TextType.TEXT)
    with_images = split_nodes_image([root_node])
    with_links = split_nodes_link(with_images)
    with_bold = split_nodes_delimiter(with_links, "**", TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold, "_", TextType.ITAL)
    nodes_list = split_nodes_delimiter(with_italic, "`", TextType.CODE) # with code
    return nodes_list


def markdown_to_blocks(markdown):
    clean_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            clean_blocks.append(stripped)
    return clean_blocks