import unittest
from splitnode import (
    extract_markdown_images,
    extract_markdown_links,
)
from markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
)

class TestMarkdown(unittest.TestCase):
    unittest.TestCase.maxDiff = None
###################################################################################
#
#  Extraction tests
#
###################################################################################
     
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_plaintext(self):
        matches = extract_markdown_images("This is imageless text.")
        expected = []
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_linkss_plaintext(self):
        matches = extract_markdown_images("This is linkless text.")
        expected = []
        self.assertListEqual(expected, matches)

###################################################################################
#
#  Markdown to blocks tests
#
###################################################################################


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_with_gap(self):
        md = """
This is **bolded** paragraph






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )





###################################################################################
#
#  BLOCK TO BLOCK TYPE TESTS
#
###################################################################################

    def test_paragraph_block(self):
        block = "This is a normal text block. Happy Path"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_block1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_block2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_block3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_block6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_block7(self):
        # too many #s according to spec, return plain para
        block = "####### Heading 7 not supported"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```let x = 1\nsum = x + oldsum\n return sum```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_bad_code_block(self):
        # missing ending 3 backticks
        block = "```let x = 1\nsum = x + oldsum\n return sum"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = ">This is a quote\n>with each line\n>starting correctly"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_bad_quote_block(self):
        block = "> Quoted\nlike a\n quote should\n> quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- First Item\n- Second\n- Third\n- Fourth"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_bad_unordered_list_block(self):
        # third item missing "- ""
        block = "- First Item\n- Second\nThird\n- Fourth"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. One\n2. Two\n3. Three\n4. Four"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_out_of_order_list_block(self):
        block = "1. One\n5. Five\n2. Two\n3. Three\n4. Four"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_missing_number_ordered_list_block(self):
        block = "1. One\n3. Three\n4. Four"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


#####################################################################################################

#
# Tests for md to html nodes

# VERY IMPORTANT: the triple-quoted stuff has to have zero indent, or the 4 chars of space gets
# inserted 
#####################################################################################################
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list_links(self):
        md = """
- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
 """       
        node = markdown_to_html_node(md) 
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><a href=\"/blog/glorfindel\">Why Glorfindel is More Impressive than Legolas</a></li><li><a href=\"/blog/tom\">Why Tom Bombadil Was a Mistake</a></li></ul></div>"
        )


    def test_heading1(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1></div>"
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


    def test_link_block(self):
        md = "Want to get in touch? [Contact me here](/contact)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Want to get in touch? <a href=\"/contact\">Contact me here</a>.</p></div>"
        )

    def test_other_link_block(self):
        md = "This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This site was generated with a custom-built <a href=\"https://www.boot.dev/courses/build-static-site-generator-python\">static site generator</a> from the course on <a href=\"https://www.boot.dev\">Boot.dev</a>.</p></div>"
        )


if __name__ == "__main__":
    unittest.main()
