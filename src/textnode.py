from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(textnode):
     
        if textnode.text_type ==TextType.TEXT:
            return LeafNode(None,textnode.text)
        
        elif textnode.text_type ==  TextType.BOLD:
            return LeafNode("b", textnode.text)
        
        elif textnode.text_type == TextType.ITALIC:
            return LeafNode("i", textnode.text)
        
        elif textnode.text_type == TextType.CODE:
            return LeafNode("code", textnode.text)
        
        elif  textnode.text_type == TextType.LINK:
            #urlval = f'{textnode.url}'
            props = {"href": textnode.url}
            return LeafNode("a", textnode.text, props)
        
        elif textnode.text_type ==  TextType.IMAGE:
            props = {"src": textnode.url, "alt": textnode.text,}
           # src = f" src='{textnode.url}'"
            #alttext = f"alt='{textnode.text}'"
            #props = [src, alttext]
            return LeafNode("img", None, props)
        
        else:
            raise Exception("invalid text type")
        

    """   
    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
"""
    def __eq__ (self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
