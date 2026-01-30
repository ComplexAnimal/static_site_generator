import unittest

from textnode import TextNode, TextType
from md_parser import (split_nodes_delimiter, extract_markdown_images,
                       extract_markdown_links, split_nodes_image, split_nodes_link,
                       text_to_text_nodes, markdown_to_blocks, block_to_block_type,
                       BlockType)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_only_non_text_tags(self): # nodes should remain unchanged
        node1 = TextNode("Bold_text", TextType.BOLD)
        node2 = TextNode("Italic_text", TextType.ITAL)
        node3 = TextNode("Some_code", TextType.CODE)
        nodes = [node1, node2, node3]
        actual_result = split_nodes_delimiter(nodes, "_", TextType.ITAL)
        self.assertEqual(actual_result, nodes)

    def test_valid_italics(self):
        node1 = TextNode("This text has _one italic_ section.", TextType.TEXT)
        node2 = TextNode("_This text_ has two _italic sections._", TextType.TEXT)
        nodes = [node1, node2]
        expected_result = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("one italic", TextType.ITAL),
            TextNode(" section.", TextType.TEXT),
            TextNode("This text", TextType.ITAL),
            TextNode(" has two ", TextType.TEXT),
            TextNode("italic sections.", TextType.ITAL),
        ]
        actual_result = split_nodes_delimiter(nodes, "_", TextType.ITAL)
        self.assertEqual(expected_result, actual_result)

    def test_invalid_italics(self): # italics with missing closing delimiter
        node = TextNode("This text is _missing a delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITAL)

    def test_bold_text(self):
        node = TextNode("This is **bold** text.", TextType.TEXT)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        actual_result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected_result, actual_result)

    def test_inline_code(self):
        node = TextNode("This line `has code` in it.", TextType.TEXT)
        expected_result = [
            TextNode("This line ", TextType.TEXT),
            TextNode("has code", TextType.CODE),
            TextNode(" in it.", TextType.TEXT),
        ]
        actual_result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(expected_result, actual_result)


class TestExtractMarkdownImagesAndLinks(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected_result = [
            ("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected_result, matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAG, "https://i.imgur.com/3elNhQu.png"),
        ]
        actual_result = split_nodes_image([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_leading_image(self):
        node = TextNode(
            "![This](https://i.imgur.com/zjjcJKZ.png) is an image",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This", TextType.IMAG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" is an image", TextType.TEXT),
        ]
        actual_result = split_nodes_image([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_trailing_image(self):
        node = TextNode(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAG, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        actual_result = split_nodes_image([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_only_image(self):
        node = TextNode(
            "![This is an image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is an image", TextType.IMAG, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        actual_result = split_nodes_image([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_multiple_nodes_with_images(self):
        node1 = TextNode(
            "This is text with ![image1](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        node2 = TextNode(
            "And here's ![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("image1", TextType.IMAG, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("And here's ", TextType.TEXT),
            TextNode("image2", TextType.IMAG, "https://i.imgur.com/3elNhQu.png"),
        ]
        actual_result = split_nodes_image([node1, node2])
        self.assertListEqual(expected_result, actual_result)

    def test_split_node_with_no_image(self):
        node = TextNode("There is no image here", TextType.TEXT)
        expected_result = [node]
        actual_result = split_nodes_image([node])
        self.assertListEqual(expected_result, actual_result)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://www.boot.dev"),
        ]
        actual_result = split_nodes_link([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_leading_link(self):
        node = TextNode(
            "[This](https://www.google.com) is a link",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This", TextType.LINK, "https://www.google.com"),
            TextNode(" is a link", TextType.TEXT),
        ]
        actual_result = split_nodes_link([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_trailing_link(self):
        node = TextNode(
            "This is a [link](https://www.google.com)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
        ]
        actual_result = split_nodes_link([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_only_link(self):
        node = TextNode(
            "[This is a link](https://www.google.com)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is a link", TextType.LINK, "https://www.google.com"),
        ]
        actual_result = split_nodes_link([node])
        self.assertListEqual(expected_result, actual_result)

    def test_split_multiple_nodes_with_links(self):
        node1 = TextNode(
            "This is text with [link1](https://www.google.com)",
            TextType.TEXT
        )
        node2 = TextNode(
            "And here's [link2](https://www.boot.dev)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://www.google.com"),
            TextNode("And here's ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://www.boot.dev"),
        ]
        actual_result = split_nodes_link([node1, node2])
        self.assertListEqual(expected_result, actual_result)

    def test_split_node_with_no_link(self):
        node = TextNode("There is no link here", TextType.TEXT)
        expected_result = [node]
        actual_result = split_nodes_link([node])
        self.assertListEqual(expected_result, actual_result)


class TestTextToTextNodes(unittest.TestCase):
    def test_with_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITAL),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual_result = text_to_text_nodes(text)
        self.assertListEqual(expected_result, actual_result)

    def test_with_only_plain_text(self):
        text = "This is just plain text"
        expected_result = [TextNode(text, TextType.TEXT)]
        actual_result = text_to_text_nodes(text)
        self.assertListEqual(expected_result, actual_result)

    def test_with_multiple_bold_and_no_plain(self):
        text = "**This is ****text**** with only bold text and an **![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)** and a **[link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode(" with only bold text and an ", TextType.BOLD),
            TextNode("obi wan image", TextType.IMAG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.BOLD),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual_result = text_to_text_nodes(text)
        self.assertListEqual(expected_result, actual_result)

    def test_with_missing_delimiter(self):
        text = "This is **text** with an _italic_ word and a `code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(Exception):
            text_to_text_nodes(text)

    def test_with_delimiters_in_link(self):
        text = "This [link**](https://www.has_delimiters.org) has _delimiters_ in it"
        expected_result = [
            TextNode("This ", TextType.TEXT),
            TextNode("link**", TextType.LINK, "https://www.has_delimiters.org"),
            TextNode(" has ", TextType.TEXT),
            TextNode("delimiters", TextType.ITAL),
            TextNode(" in it", TextType.TEXT),
        ]
        actual_result = text_to_text_nodes(text)
        self.assertEqual(expected_result, actual_result)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_clean_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_excessive_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_leading_and_trailing_newlines(self):
        md = """



This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_leading_and_trailing_spaces(self):
        md = """
    This is **bolded** paragraph   

  This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line      

 - This is a list
- with items   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_with_min_hashes(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_with_max_hashes(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_with_extra_spaces(self):
        block = "###   Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_missing_space(self): # should be paragraph
        block = "#####Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self): # should be paragraph
        block = "####### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_empty(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_clean(self):
        block = "```\nThis is some code\nThe code keeps going```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_missing_a_backtick(self): # should be paragraph
        block = "```\nThis is bad code``"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_missing_newline(self): # should be paragraph
        block = "```This is bad code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_with_extra_newlines(self):
        block = "```\n\nThis is some code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_clean(self):
        block = ">This is a quote\n> This is another\n>      Here's yet another"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_blank_lines(self):
        block = "> This quote has\n>\n>\n> some empty lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_missing_character(self): # should be paragraph
        block = "> This is a quote\n This is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_clean(self):
        block = "- This\n- is\n- an\n- unordered\n- list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_blank_lines(self):
        block = "- This\n- has\n- \n- blank\n- \n- lines"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_extra_spaces(self):
        block = "- This\n-  list\n-   has\n-    extra\n-     spaces "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_character(self): # should be paragraph
        block = "- This\n- isn't\n a\n- list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_missing_space(self): # should be paragraph
        block = "- This\n-isn't\n- a\n- list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_clean(self):
        block = "1. This list\n2. has three\n3. lines"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_with_wrong_number(self): # should be paragraph
        block = "1. This\n2. is\n5. wrong"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_missing_number(self): # should be paragraph
        block = "1. This is\n2. missing a\n. number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_missing_period(self): # should be paragraph
        block = "1. This is\n2 missing a\n3. period"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_missing_space(self): # should be paragraph
        block = "1.This\n2. is\n3. wrong"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_starts_with_space(self): # should be paragraph
        block = " 1. Not\n2. a\n3. list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()