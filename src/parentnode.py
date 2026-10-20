
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag:str | None, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
