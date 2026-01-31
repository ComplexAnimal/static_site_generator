import unittest

from md_to_html import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestMarkdownToHTML(unittest.TestCase):

    def test_headings(self):
        md = """
# Heading 1

### Heading 3

###### Heading 6

####    Heading with extra spaces   

## **Bold heading**

######## Paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3</h3><h6>Heading 6</h6><h4>Heading with extra spaces</h4><h2><b>Bold heading</b></h2><p>######## Paragraph</p></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quotes(self):
        md = """
>Quote without space

> Quotes with space
>    and extra spaces   

> Quotes with **bold text**,
> _italic text_,
> and a [link](https://www.google.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                '<div><blockquote>Quote without space</blockquote>'
                '<blockquote>Quotes with space\n'
                'and extra spaces</blockquote>'
                '<blockquote>Quotes with <b>bold text</b>,\n'
                '<i>italic text</i>,\n'
                'and a <a href="https://www.google.com">link</a></blockquote></div>'
            )
        )

    def test_unordered_list(self):
        md = """
- Just a list
- with 2 lines

-    This list has
- extra spaces     

- **Bold text**
- _Italic text_
- Plain text

- This is not
-a list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                "<div><ul><li>Just a list</li><li>with 2 lines</li></ul>"
                "<ul><li>This list has</li><li>extra spaces</li></ul>"
                "<ul><li><b>Bold text</b></li><li><i>Italic text</i></li>"
                "<li>Plain text</li></ul><p>- This is not -a list</p></div>"
            )
        )

    def test_ordered_list(self):
        md = """
1. This list
2. has three
3. lines

1.     This list has
2. extra spaces     

1. **Bold**
2. _Italic_

1. [A link](https://www.google.com)
2. ![An image](https://www.an_image.com)

1 No list here

1.Not here either

2. Nope

1. Skip
3. two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                '<div><ol><li>This list</li><li>has three</li><li>lines</li></ol>'
                '<ol><li>This list has</li><li>extra spaces</li></ol>'
                '<ol><li><b>Bold</b></li><li><i>Italic</i></li></ol>'
                '<ol><li><a href="https://www.google.com">A link</a></li>'
                '<li><img src="https://www.an_image.com" alt="An image"></li></ol>'
                '<p>1 No list here</p><p>1.Not here either</p><p>2. Nope</p>'
                '<p>1. Skip 3. two</p></div>'
            )
        )


    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
