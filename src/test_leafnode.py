import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_no_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")

    def test_leaf_repr_no_props(self):
        tag = "p"
        value = "Hello, world!"
        props = None
        node = LeafNode(tag, value)
        expected = f"LeafNode({tag}, {value}, {props})"
        self.assertEqual(repr(node),expected)

    def test_leaf_repr_with_props(self):
        tag = "a"
        value = "Click me!"
        props = {"href": "https://www.google.com"}
        node = LeafNode(tag, value, props)
        expected = f"LeafNode({tag}, {value}, {props})"
        self.assertEqual(repr(node),expected)


if __name__ == "__main__":
    unittest.main()
