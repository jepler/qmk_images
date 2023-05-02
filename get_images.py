import requests
import hashlib
import urllib
import traceback
from markdown_it import MarkdownIt
import pathlib

cache_path = pathlib.Path(__file__).parent / "images"

def get_images(tokens):
    """Flattens the token stream."""
    for token in tokens:
        if token.tag == "img":
            yield token.attrs['src']
        if token.children is not None:
            yield from get_images(token.children)

def cache_image(url):
    qurl = urllib.parse.quote(url, safe='')
    subdir = hashlib.sha256(qurl.encode("utf-8")).hexdigest()[:2]
    local = cache_path / subdir / qurl
    if local.exists():
        return
    local.parent.mkdir(parents=True, exist_ok=True)
    print(local)
    try:
        response = requests.get(url)
        with open(local, "wb") as f:
            f.write(response.content)
    except Exception as e:
        traceback.print_exc()

qmk_firmware = pathlib.Path("/home/jepler/src/qmk_firmware")

parser = MarkdownIt("gfm-like")
for filename in qmk_firmware.glob("**/*.md"):
    print(filename)
    with open(filename, encoding="utf-8") as f:
        parsed = parser.parse(f.read())
        for g in get_images(parsed):
            print(g)
#            if 'imgur' in g:
#                cache_image(g)
