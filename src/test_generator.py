
import unittest

from generator import extract_title, replace_placeholder

class TestMarkdown(unittest.TestCase):

    def test_extract_title(self):
        md = "\n\n# My Title Is Huge\n\nIt sure is\n"
        self.assertEqual(extract_title(md), "My Title Is Huge") 

    def test_extract_title_strip(self):
        md = "\n\n# My Title Is Huge    \n\nIt sure is\n"
        self.assertEqual(extract_title(md), "My Title Is Huge") 

    def test_extract_title_strip2(self):
        md = "\n\n#     My Title Is Huge    \n\nIt sure is\n"
        self.assertEqual(extract_title(md), "My Title Is Huge") 

    def test_replace_placeholder(self):
        source = "<title>{{Title}}</title>"
        replaced = replace_placeholder(source, "{{Title}}", "My Title")
        self.assertEqual(replaced, "<title>My Title</title>")