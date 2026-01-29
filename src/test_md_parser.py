import unittest

from textnode import TextNode, TextType
from md_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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


if __name__ == "__main__":
    unittest.main()