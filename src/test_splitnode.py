import unittest
from splitnode import (
    split_nodes_delimiter,
)
from textnode import TextNode, TextType
 

class TestSplitNode(unittest.TestCase):

    def test_split_bold_node(self):
        node = TextNode("This is text with **bold and refreshing** inline", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold and refreshing", TextType.BOLD),
                TextNode(" inline", TextType.TEXT),
            ]
        )

    def test_split_italic_node(self):
        node = TextNode("This is text with _shiny italics_ inline", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is text with ", TextType.TEXT),
                TextNode("shiny italics", TextType.ITALIC),
                TextNode(" inline", TextType.TEXT),
            ]
        )

    def test_split_code_node(self):
        node = TextNode("This is text with `code` inline", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" inline", TextType.TEXT),
            ]
        )

    def test_plain_text_nodes(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is just plain text", TextType.TEXT),
            ]
        )

    def test_italic_node_passthru(self):
        node = TextNode("This is just _italic_ text", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is just _italic_ text", TextType.ITALIC),
            ]
        )


    def test_bold_node_passthru(self):
        node = TextNode("This is just _italic_ text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is just _italic_ text", TextType.BOLD),
            ]
        )

    def test_code_node_passthru(self):
        node = TextNode("This is just _italic_ text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This is just _italic_ text", TextType.CODE),
            ]
        )

    def test_two_split_bold_node(self):
               
        node = TextNode("This **is** just **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" just ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )


