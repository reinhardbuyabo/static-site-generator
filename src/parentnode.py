from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")

        if self.children is None:
            raise ValueError("children is/are missing")

        hm = ""
        for child in self.children:
            hm += child.to_html()

        return f'<{self.tag}>{hm}</{self.tag}>'
