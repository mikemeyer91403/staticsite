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
        

        '''
     def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes: a list of nodes
    # delimiter: a delimiter to scan for  (e.g. ', **, _)
    # text_type  The TextType (e.g. CODE, TEXT, etc.) of the nodes inside the delimiter
    # returns: new list of nodes, where text nodes are potentially split into multiple text
    # nodes.

    # This method should handle inline bold, italic, and code blocks.
        output = []
        inline_type = TextType.TEXT
        if delimiter == "`":
            inline_type = TextType.CODE
        elif delimiter =="_":
            inline_type = TextType.ITALIC
        elif delimiter == "**":
            inline_type = TextType.BOLD

        #print(f"old nodes: {old_nodes}")
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                output.append(node)
                continue
            split_strings = node.text.split(delimiter)
            #print(f"split strings: {split_strings}")
            if len(split_strings) % 2 == 0:
                raise Exception("closing delimiters not found")

            new_nodes = []
            for i in  range (len(split_strings)):
                if i % 2 == 0:
                    new_nodes.append( TextNode (split_strings[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_strings[i], inline_type))
            #print(f"new nodes: {new_nodes}")
            output.extend(new_nodes)
        #print(f"final_output: {output}")
        return(output)
        '''

    def __eq__ (self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
   
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
