import unittest

from textnode import TextNode, TextType
from md_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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
            TextNode("", TextType.TEXT),
            TextNode("This text", TextType.ITAL),
            TextNode(" has two ", TextType.TEXT),
            TextNode("italic sections.", TextType.ITAL),
            TextNode("", TextType.TEXT),
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


if __name__ == "__main__":
    unittest.main()