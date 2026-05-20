class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # p a h1
        self.value = value  # text inside p
        self.children = children  # list of HTMLNode objects
        self.props = props  # dictionary of k, v pairs

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        hm = ""
        if self.props is None:
            return hm
        if self.props:
            for k, v in self.props.items():
                hm += f' {k}="{v}"'
        return hm

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
