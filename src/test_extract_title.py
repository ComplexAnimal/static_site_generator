import unittest

from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_heading_at_top(self):
        md = """
# Heading
some stuff
"""
        result = extract_title(md)
        self.assertEqual(result, "Heading")

    def test_heading_in_middle(self):
        md = """
some stuff
# Heading
some more stuff
"""
        result = extract_title(md)
        self.assertEqual(result, "Heading")

    def test_heading_with_extra_spaces(self):
        md = """
#     Heading    
some stuff
"""
        result = extract_title(md)
        self.assertEqual(result, "Heading")

    def test_missing_heading(self):
        md = """
some stuff
## h2 heading
even more stuff
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_displaced_heading(self):
        md = """
 # Space before hash
 #### h4 heading
 """
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()