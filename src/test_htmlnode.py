import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_create_html_node_empty(self):
        node = HTMLNode()
        expected = "HTMLNode(None, None, None, None)"
        self.assertEqual(repr(node), expected)

    def test_create_html_node_with_children(self):
        link1 = HTMLNode("a", "Click here", None, {"href": "www.boots.dev"})
        link2 = HTMLNode("a", "Click here", None, {"href": "www.google.com"})
        body = HTMLNode("body", None, [link1, link2], None)
        expected = "HTMLNode(body, None, [HTMLNode(a, Click here, None, {'href': 'www.boots.dev'}), HTMLNode(a, Click here, None, {'href': 'www.google.com'})], None)"
        self.assertEqual(repr(body), expected)

    def test_props_to_html_with_props(self):
        tag = "a"
        value = "Click here"
        children = None
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag, value, children, props)
        expected =  ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        tag = "a"
        value = "Click here"
        children = None
        props = None
        node = HTMLNode(tag, value, children, props)
        expected =  ''

        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
