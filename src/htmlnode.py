class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props= None):
        self.tag = tag  # string representing HTML tag name
        self.value = value  #string with text in the tag
        self.children = children #list of children of node
        self.props = props   # dict of tag attributes
        # note: each node either has a value or children

    def to_html(self):
        raise NotImplementedError
        return None
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        output = ""
        for key in self.props:
            output += f" {key}=\"{self.props[key]}\""
        return output
    
    def __repr__(self):
        return f"HTMLNode ({self.tag}, {self.value}, children:{self.children} props:{self.props})"
    