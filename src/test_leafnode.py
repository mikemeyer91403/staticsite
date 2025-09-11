import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link", {"href":"https://www.apple.com","target":"_blank",})
        expected = '<a href="https://www.apple.com" target="_blank">This is a link</a>'
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "This is just text")
        expected = "This is just text"
        self.assertEqual(node.to_html(), expected)

    #TODO: add a test for the __repr__method

