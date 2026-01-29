import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            split_nodes = node.text.split(delimiter)

            if len(split_nodes) < 3 or len(split_nodes) % 2 == 0:
                raise Exception("Error: The text is missing a closing delimiter")
            
            else:
                node_group = []

                for i in range(len(split_nodes)):

                    if i % 2 == 0: # Should always be plain text
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

