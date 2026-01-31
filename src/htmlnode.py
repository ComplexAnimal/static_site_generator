class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Error: Method must be overridden by child class")
    
    def props_to_html(self):
        result = ""
        if not self.props:
            return result
        for k, v in self.props.items():
            result += f' {k}="{v}"'
        return result
    
    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Error: Leaf nodes must have a value")
        if not self.tag:
            return self.value
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        elif self.tag == "a": # link
            return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        else: # image
            return f'<{self.tag}{super().props_to_html()}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Error: Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("Error: Parent nodes must have children")
        else:
            return f"<{self.tag}>" + "".join(child.to_html() for child in self.children) + f"</{self.tag}>"
