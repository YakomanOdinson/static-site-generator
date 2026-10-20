import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        if  text.count(delimiter) % 2 != 0:
            raise ValueError("The markdown is malformed. There is no matching closing delimiter " + delimiter)

        text_pieces = text.split(delimiter)
        for i in range(len(text_pieces)):
            if text_pieces[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text_pieces[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_pieces[i], text_type))
        # if len(text_pieces) == 1:
        #     new_nodes.append(TextNode(text_pieces[0], TextType.TEXT))
        # else:
        #     if text_pieces[0]:
        #         new_nodes.append(TextNode(text_pieces[0], TextType.TEXT))
        #     new_nodes.append(TextNode(text_pieces[1], text_type))
        #     if text_pieces[2]:
        #         new_nodes.append(TextNode(text_pieces[2], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(len(images)):
            image_alt, image_link = images[i]
            delimiter = f"![{image_alt}]({image_link})"
            sections = text.split(delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            before_text, after_text = sections
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if after_text:
                if i < (len(images)):
                    text = after_text
                else:
                    new_nodes.append(TextNode(after_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for i in range(len(links)):
            link_text, link_url = links[i]
            delimiter = f"[{link_text}]({link_url})"
            sections = text.split(delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            before_text, after_text = sections
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if after_text:
                if i < (len(links) - 1):
                    text = after_text
                else:
                    new_nodes.append(TextNode(after_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
