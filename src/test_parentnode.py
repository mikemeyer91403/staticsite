import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        #print()
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_parent_to_html_p(self):
        child_node1 = LeafNode("b","Boldly GO")
        child_node2 = LeafNode("i", "italic")
        children = [child_node1,child_node2]
        pnode = ParentNode("p",children)
        self.assertEqual(pnode.to_html(), "<p><b>Boldly GO</b><i>italic</i></p>")
    
    def test_parent_repr(self):
        child_node1 = LeafNode("b","Boldly GO")
        child_node2 = LeafNode("i", "italic")
        children = [child_node1,child_node2]
        pnode = ParentNode("p",children)
        #print(pnode)
        expected = 'ParentNode(p, children:[LeafNode(b, Boldly GO, props:None), LeafNode(i, italic, props:None)], props:None)'
        self.assertEqual(pnode.__repr__(), expected)