#import textnode
from textnode import TextNode, TextType



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
    return output



