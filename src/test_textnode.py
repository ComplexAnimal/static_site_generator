import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text(self):
        node = TextNode("This is a word", TextType.ITAL)
        node2 = TextNode("These are words", TextType.ITAL)
        self.assertNotEqual(node, node2)

    def test_eq_with_link(self):
        node = TextNode("This is a link", TextType.LINK, "https:www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https:www.boot.dev")
        self.assertEqual(node, node2)

    def test_dif_text_type(self):
        node = TextNode("This is a link", TextType.LINK, "https:www.boot.dev")
        node2 = TextNode("This is a link", TextType.IMAG, "https:www.boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()