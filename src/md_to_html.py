from md_parser import (
    markdown_to_blocks, block_to_block_type,
    text_to_text_nodes, BlockType
)
from textnode import TextNode, text_node_to_html_node, TextType
from htmlnode import ParentNode


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    root_tag = "div"
    children = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                block_node = heading_to_html_node(block)
            case BlockType.PARAGRAPH:
                block_node = paragraph_to_html_node(block)
            case BlockType.QUOTE:
                block_node = quote_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                block_node = unordered_list_to_html_node(block)
            case BlockType.ORDERED_LIST:
                block_node = ordered_list_to_html_node(block)
            case BlockType.CODE:
                block_node = code_to_html_node(block)
            case _:
                raise Exception("Error: Block is not a valid BlockType")
        children.append(block_node)
    return ParentNode(root_tag, children)


def heading_to_html_node(block):
    count = 0
    i = 0
    while block[i] == "#":
        count += 1
        i += 1
    tag = f'h{count}'
    text = block[i:].strip()
    text_nodes = text_to_text_nodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return ParentNode(tag, children)

def paragraph_to_html_node(block):
    tag = 'p'
    text = block.replace("\n", " ").strip()
    text_nodes = text_to_text_nodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return ParentNode(tag, children)

def quote_to_html_node(block):
    tag = 'blockquote'
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        stripped = line[1:].strip()
        new_lines.append(stripped)
    text = "\n".join(new_lines)
    text_nodes = text_to_text_nodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return ParentNode(tag, children)

def unordered_list_to_html_node(block):
    block_tag = 'ul'
    line_tag = 'li'
    lines = block.split("\n")
    list_children = []
    for line in lines:
        text = line[1:].strip()
        line_nodes = text_to_text_nodes(text)
        line_children = []
        for node in line_nodes:
            line_children.append(text_node_to_html_node(node))
        line_html = ParentNode(line_tag, line_children)
        list_children.append(line_html)
    return ParentNode(block_tag, list_children)
        
def ordered_list_to_html_node(block):
    block_tag = 'ol'
    line_tag = 'li'
    lines = block.split("\n")
    list_children = []
    for line in lines:
        text = line[2:].strip()
        line_nodes = text_to_text_nodes(text)
        line_children = []
        for node in line_nodes:
            line_children.append(text_node_to_html_node(node))
        line_html = ParentNode(line_tag, line_children)
        list_children.append(line_html)
    return ParentNode(block_tag, list_children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(text_node)
    return ParentNode("pre", [child])
