import htmlnode

from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, value, tag, props=None):
        self = super().__init__(value, tag, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value 
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, props:{self.props})"
  