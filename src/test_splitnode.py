import unittest
from splitnode import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType
 

class TestSplitNode(unittest.TestCase):

########################################
#
#  Inline text node splitting tests
#
########################################

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
    
    def test_split_bold_single(self):
        node = TextNode("**bold and refreshing**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [ 
                TextNode("bold and refreshing", TextType.BOLD),
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

#####################################################
#
#  Image and Link processing
#
#####################################################

    def test_split_images(self):
        node = TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
             "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
             TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(new_nodes, expected)


############################################
#
#  Text to TextNodes Tests
#
############################################


    def test_text_to_nodes_plaintext(self):
        text  = "This is just plain old simple text with no markdown"
        new_nodes = text_to_textnodes(text)
        expected =  [
                TextNode("This is just plain old simple text with no markdown", 
                         TextType.TEXT
                         ),

            ]
        self.assertListEqual(new_nodes, expected)
    
    def test_text_to_nodes_just_bold(self):
        text = "**Going Boldly For You**"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Going Boldly For You", TextType.BOLD),
            ],
            new_nodes
        )

    def test_text_to_nodes_just_italic(self):
        text = "_this is just in italics_"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("this is just in italics", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_text_to_nodes_just_code(self):
        text = "`this is just in Code`"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("this is just in Code", TextType.CODE),
            ],
            new_nodes
        )

    def test_text_to_nodes_all1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_nodes_all_trailing(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and some text afterwards."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and some text afterwards.", TextType.TEXT),

            ],
            new_nodes
        )    