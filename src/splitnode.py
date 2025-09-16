#import textnode
from textnode import TextNode, TextType
from markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes: a list of nodes
    # delimiter: a delimiter to scan for  (e.g. ', **, _)
    # text_type  The TextType (e.g. CODE, TEXT, etc.) of the nodes inside the delimiter
    # returns: new list of nodes, where text nodes are potentially split into multiple text
    # nodes.

    # This method should handle inline bold, italic, and code blocks.
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        split_strings = node.text.split(delimiter)
        if len(split_strings) % 2 == 0:
            raise Exception("closing delimiters not found")
        new_nodes = []
        for i in  range (len(split_strings)):
            if split_strings[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append( TextNode (split_strings[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_strings[i], text_type))
            #print(f"new nodes: {new_nodes}")
        output.extend(new_nodes)
        #print(f"final_output: {output}")
    return output


def split_nodes_image(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT: #passthru
            new_nodes.append(old)
            continue
        old_text = old.text
        img_results = extract_markdown_images(old_text)
        #print( f"img_results: {img_results}")
        #passthru node if no images in it
        if len(img_results) == 0:
            new_nodes.append(old)
            continue
        for result in img_results:
            sections = old_text.split(f"![{result[0]}]({result[1]})", 1)
            if len (sections) != 2:
                raise ValueError("invalid markdown")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(
                TextNode(
                    result[0],
                    TextType.IMAGE,
                    result[1]
                )
            )
            old_text = sections[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
       # print (f"new_nodes:\n {new_nodes}")
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
            continue
        links= extract_markdown_links(old.text)
        if links == []:
            new_nodes.append(old)
            continue
        old_text = old.text
        for result in links:
            sections = old_text.split(f"[{result[0]}]({result[1]})", 1)
            if len (sections) != 2:
                raise ValueError("invalid markdown")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
                new_nodes.append(
                    TextNode(
                        result[0],
                        TextType.LINK,
                        result[1]
                    )
                )
            old_text = sections[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    new_nodes = [ TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes



