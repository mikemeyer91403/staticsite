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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")


    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://www.apple.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props,{"href":"http://www.apple.com",})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://www.mikemeyer.net/img/foo.gif")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props,{"src": "http://www.mikemeyer.net/img/foo.gif", "alt": "This is an image"})

"""
TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""

if __name__ == "__main__":
    unittest.main()
