from textnode import TextNode
from textnode import TextType

def main():
    newnode = TextNode("My italics text", TextType.ITALIC.value, "http://www.boot.dev")
    print(newnode)

main()