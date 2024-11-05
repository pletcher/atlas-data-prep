#!/usr/bin/env python3

import json
from pathlib import Path
import re

from lxml import etree

CANONICAL_ENGLIT = Path(__file__).parent.parent.parent.parent / "canonical-engLit"


def text_content(el):
    return re.sub(r"\s+", " ", "".join(el.xpath(".//text()"))).strip()


class Converter:

    def convert_othello(self, filename):
        # we have to do this because there are undeclared entities
        parser = etree.XMLParser(load_dtd=False, no_network=True, resolve_entities=False)

        root = etree.parse(filename, parser=parser).getroot()

        body = root.xpath("/TEI.2/text/body")[0]
        for child in body:
            assert child.tag == "div1"
            assert child.attrib["type"] == "act"
            if child.attrib["n"] == "cast":
                # no-op for now but we could extract the case list as metadata
                pass
            else:
                yield from self.handle_act(child)


    def handle_act(self, el):
        self.act_num = int(el.attrib["n"])
        self.scene_num = 0
        self.line_num = 0
        assert el[0].tag == "head"
        yield from self.handle_head(el[0])
        for child in el[1:]:
            if child.tag == "lb":
                pass
            else:
                assert child.tag == "div2"
                assert child.attrib["type"] == "scene"
                yield from self.handle_scene(child)


    def handle_scene(self, el):
        self.scene_num = int(el.attrib["n"])
        self.who = None
        self.line_num = 0
        assert el[0].tag == "head"
        self.handle_head(el[0])
        for child in el[1:]:
            if child.tag == "lb":
                pass
            elif child.tag == "stage":
                yield from self.handle_stage(child)
            else:
                assert child.tag == "sp"
                yield from self.handle_speech(child)


    def handle_head(self, el):
        assert el.attrib == {}
        ref = self.get_ref()
        yield ref, {"kind": "head"}, text_content(el)


    def handle_speech(self, el):
        assert el[0].tag == "speaker"
        self.who = el.attrib["who"]
        for child in el[1:]:
            if child.tag == "lb":
                pass
            elif child.tag == "stage":
                yield from self.handle_stage(child)
            elif child.tag == "p":
                yield from self.handle_prose(child)
            else:
                assert child.tag == "l"
                yield from self.handle_line(child)
        self.who = None


    def get_ref(self):
        return f"{self.act_num}.{self.scene_num}.{self.line_num}"


    def handle_stage(self, el):
        assert el.attrib.get("type") in ["setting", "entrance", None]
        annotations = {"kind": "stage"}
        if self.who:
            annotations["who"] = self.who
        if el.attrib.get("type"):
            annotations["type"] = el.attrib["type"]
        self.line_num += 1
        ref = self.get_ref()
        yield ref, annotations, text_content(el)


    def handle_prose(self, el):
        assert el.attrib == {}
        annotations = {"kind": "prose"}
        if self.who:
            annotations["who"] = self.who
        self.line_num += 1
        ref = self.get_ref()
        yield ref, annotations, text_content(el)


    def handle_line(self, el):
        annotations = {"kind": "line"}
        if self.who:
            annotations["who"] = self.who
        if el.attrib.get("part"):
            annotations["part"] = el.attrib["part"]
        self.line_num += 1
        ref = self.get_ref()
        yield ref, annotations, text_content(el)


if __name__ == "__main__":
    c = Converter()
    filename = CANONICAL_ENGLIT / "Renaissance/Shakespeare/opensource/oth.xml"
    with open("othello-text.tsv", "w") as text_fd, open("othello-anno.jsonl", "w") as anno_fd:
        for ref, annotations, content in c.convert_othello(filename):
            print(ref, content, sep="\t", file=text_fd)
            annotations["ref"] = ref
            print(json.dumps(annotations), file=anno_fd)
