import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.apple.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://www.apple.com")
        self.assertNotEqual(node, node2)

    def test_nullurl(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = TextNode("This is an apple", TextType.BOLD)
        node2 = TextNode("This is an orange", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = TextNode("This is an apple", TextType.BOLD, "http://mikemeyer.net")
        node2 = TextNode("This is an apple", TextType.BOLD, "http://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_neq_url_none(self):
        node1 = TextNode("This is an apple", TextType.BOLD, "http://mikemeyer.net")
        node2 = TextNode("This is an apple", TextType.BOLD)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
