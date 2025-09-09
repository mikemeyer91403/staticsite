import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("link", "This is a link", None, {"href": "https://www.apple.com","target":"_blank",})
        expected = " href=\"https://www.apple.com\" target=\"_blank\""
        props = node.props_to_html()
        self.assertEqual(expected, props)

    def test_props_none(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        props = node.props_to_html()
        self.assertIsNone(props)

    def test_repr(self):
        node = HTMLNode("link", "This is a link", None, {"href": "https://www.apple.com","target":"_blank",})
        #expected =  f"HTMLNode ({self.tag} {self.value} children:{self.children} props:{self.props}"

        expected = "HTMLNode (link, This is a link, children:None props:{'href': 'https://www.apple.com', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected)
    
    """
    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        
        with self.assertRaises(NotImplementedError, "not implemented"):
            result = node.to_html()
            print ("not implmented")
    """

if __name__ == "__main__":
    unittest.main()
