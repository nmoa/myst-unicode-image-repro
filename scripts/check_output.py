#!/usr/bin/env python3
"""Verify image references in generated HTML point to existing copied assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

class ImageCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = {}

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            data = dict(attrs)
            if data.get("alt") and data.get("src"):
                self.images[data["alt"]] = data["src"]

def main():
    html = Path(sys.argv[1] if len(sys.argv) > 1 else "_build/html/index.html")
    if not html.is_file():
        print(f"FAIL: HTML not generated: {html}")
        return 2
    parser = ImageCollector()
    parser.feed(html.read_text(encoding="utf-8"))
    results = {}
    for label in ("ASCII control", "Japanese filename", "Japanese directory"):
        src = parser.images.get(label)
        if src is None:
            print(f"FAIL [{label}]: missing img tag")
            results[label] = False
            continue
        url = urlsplit(src)
        if url.scheme or url.netloc:
            print(f"FAIL [{label}]: unexpected external URL: {src}")
            results[label] = False
            continue
        expected = html.parent / unquote(url.path)
        results[label] = expected.is_file()
        print(f"{'PASS' if results[label] else 'FAIL'} [{label}]: src={src}, expected={expected}")
    print("Generated PNG files:")
    for path in sorted(html.parent.rglob("*.png")):
        print(f"  {path.relative_to(html.parent)}")
    if not results.get("ASCII control"):
        print("ERROR: ASCII baseline failed")
        return 2
    if not all(results.values()):
        print("REPRODUCED: Unicode image path missing from output")
        return 1
    print("NOT REPRODUCED: all assets resolve")
    return 0

if __name__ == "__main__":
    sys.exit(main())
