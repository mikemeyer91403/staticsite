   
import re

def extract_markdown_images(text):
    tuple_list = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        tuple_list.append(match)
    return tuple_list

def extract_markdown_links(text):
    tuple_list = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        tuple_list.append(match)
    return tuple_list