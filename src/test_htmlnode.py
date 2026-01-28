import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("h1", "This is a header", None, None)
        node2 = HTMLNode("h1", "This is a header", None, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("p", "This is some text", "a", None)
        node2 = HTMLNode("p", "This is some text", None, {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        props_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        props_string = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode("a", "This is a link", None, props_dict)
        self.assertEqual(node.props_to_html(), props_string)

if __name__ == "__main__":
    unittest.main()