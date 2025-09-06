from textnode import TextNode
from textnode import TextType

def main():
    newnode = TextNode("My italics text", TextType.ITALICTEXT.value, "http://www.boot.dev")
    print(newnode)

main()