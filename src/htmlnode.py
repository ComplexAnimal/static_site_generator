from enum import Enum

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