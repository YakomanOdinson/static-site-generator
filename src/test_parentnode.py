import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2", {"class": "bullet", "id": "section-summary"})
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("div", [grandchild_node1, grandchild_node2], {"class": "list", "id": "headlines"})
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "section"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="section"><span><b>grandchild1</b></span><div class="list" id="headlines"><b>grandchild1</b><p class="bullet" id="section-summary">grandchild2</p></div></div>',
        )

    def test_parent_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_parent_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children")


if __name__ == "__main__":
    unittest.main()
