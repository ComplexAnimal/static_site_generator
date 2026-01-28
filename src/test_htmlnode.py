import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

        
class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        expected_result = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected_result)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link to Google", {"href": "https://www.google.com"})
        expected_result = '<a href="https://www.google.com">This is a link to Google</a>'
        self.assertEqual(node.to_html(), expected_result)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text", None)
        expected_result = "Just text"
        self.assertEqual(node.to_html(), expected_result)

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_large_family(self):
        baby1 = LeafNode("a", "link", {"href": "https://www.google.com"})
        baby2 = LeafNode("i", "italic")
        child1 = LeafNode("p", "paragraph")
        child2 = LeafNode("b", "bold")
        child3 = ParentNode("h1", [baby1, baby2])
        children = [child1, child2, child3]
        parent = ParentNode("ul", children)
        self.assertEqual(
            parent.to_html(),
            '<ul><p>paragraph</p><b>bold</b><h1><a href="https://www.google.com">link</a><i>italic</i></h1></ul>'
        )

    def test_to_html_empty_tag(self):
        child = LeafNode("p", "paragraph")
        parent = ParentNode("", [child])
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_empty_child_list(self):
        parent = ParentNode("h1", [])
        self.assertEqual(parent.to_html(), "<h1></h1>")

    def test_to_html_missing_children(self):
        parent = ParentNode("p", None)
        self.assertRaises(ValueError, parent.to_html)


if __name__ == "__main__":
    unittest.main()