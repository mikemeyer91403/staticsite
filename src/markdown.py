   
from enum import Enum
from textnode import text_node_to_html_node, TextType, TextNode 

from parentnode import ParentNode
from splitnode import (
    text_to_textnodes,
)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    rawblocks = markdown.split("\n\n")
    blocks = []
    for raw in rawblocks:
        stripped = raw.strip(' \n')
        if stripped != "":
            blocks.append(stripped)

    return blocks

def block_to_block_type(blocktext):
    if blocktext[0] == "#":
        patterns  = ("# ", '## ', '### ', '#### ', '##### ', '###### ')
        if blocktext.startswith(patterns):
            return BlockType.HEADING
    if blocktext.startswith("```") and blocktext.endswith("```"):
        return BlockType.CODE
    if blocktext.startswith(">"):
        lines = blocktext.split("\n")
        isquote = False
        for line in lines:
            if line.startswith(">"):
                isquote = True
            else:
                isquote = False
                break
        if isquote:
            return BlockType.QUOTE
    if blocktext.startswith("- "):
        lines = blocktext.split("\n")
        islist = False
        for line in lines:
            islist = line.startswith("- ")
            if islist == False:
                return BlockType.PARAGRAPH
            
        return BlockType.UNORDERED_LIST
    if blocktext.startswith("1. "):
        lines = blocktext.split("\n")
        index = 1
        isnumlist = True
        for line in lines:
            start = f"{index}. "
            isnumlist = line.startswith(start)
            if isnumlist == False:
                return BlockType.PARAGRAPH
            index += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

##################################################################
#
#  MD > Blocks >  HTML Nodes
#
##################################################################


def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        leaf = text_node_to_html_node(node)
        children.append(leaf)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
      # we need to count the #s at the beginning and assign header level
    numhash = block.count("#", 0, 6)
    tag = f"h{numhash}"
    trim = block.lstrip("# ")
    children = text_to_children(trim)
    return ParentNode(tag,children)
    

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    scrubbedtext = block[4:-3]
    textnode = TextNode(scrubbedtext, TextType.TEXT)
    child = text_node_to_html_node(textnode)
    code = ParentNode("code", [child])     
     ## <pre><code> content </code></pre>
    return ParentNode("pre",[code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines= []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
    wrapper = ParentNode("blockquote", children)
    return wrapper
   
def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    wrapper = ParentNode("ul", html_items)
    return wrapper


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    wrapper = ParentNode("ol", html_items)
    return wrapper



def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError("invalid block type")

                
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    div_node = ParentNode("div", children, None)
    return div_node