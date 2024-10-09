#!/usr/bin/env python

from pathlib import Path

from scanf import scanf

from confpoint.image_tag import ImageTag


def get_image_tags(html: str) -> tuple[ImageTag]:
    image_tags: list[ImageTag] = []
    for tag in [l for l in html.split('<') if 'img alt=' in l and 'src=' in l]:
        tag = "<" + tag
        if not (p := scanf('src="%s"', tag)):
            continue
        p: str = p[0]
        if p.startswith('/'):
            p = '.' + p
        image_tags.append(ImageTag(tag, Path(p)))
    return tuple(image_tags)


def replace_imgage_tag_for_confluence(html: str,
                                      image_tags: tuple[ImageTag]) -> str:
    output = html
    for tag in image_tags:
        output = output.replace(tag.tag, tag.to_confluence())
    return output


if __name__ == "__main__":
    TEST_HTML = '<h1>Test doc</h1>\n<p>Some text. Bla bla.</p>\n<p><img alt="img" src="/doc/20231020_163926.png" />\n<img alt="img" src="/doc/2022-03-13_18-44.gif" /></p>\n<p>Some text. Bla bla.\nSome text. Bla bla.</p>'
    print(TEST_HTML)
    print('-' * 10)
    tags = get_image_tags(TEST_HTML)
    # print(tags)
    result = replace_imgage_tag_for_confluence(TEST_HTML, tags)
    print(result)
