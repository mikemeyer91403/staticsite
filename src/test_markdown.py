import unittest

from markdown import (
    extract_markdown_images,
    extract_markdown_links
)

class TestMarkdown(unittest.TestCase):
     
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_plaintext(self):
        matches = extract_markdown_images("This is imageless text.")
        expected = []
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_linkss_plaintext(self):
        matches = extract_markdown_images("This is linkless text.")
        expected = []
        self.assertListEqual(expected, matches)


if __name__ == "__main__":
    unittest.main()
