from enum import Enum
from leafnode import LeafNode

import re


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
     
    def __eq__ (self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
   
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
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
        return LeafNode("img", "", props)
    
    else:
        raise Exception("invalid text type")
        


