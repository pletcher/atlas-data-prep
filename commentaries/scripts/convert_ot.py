#!/usr/bin/env python


import json
import re
import pathlib

from lxml import etree


SRC_FILE = pathlib.Path("../canonical_pdlrefwk/data/viaf2603144/viaf001/viaf2603144.viaf001.perseus-eng1.xml")
TEXT_URN = "urn:cts:greekLit:tlg0011.tlg004:"  # note trailing colon
DESTO_DIR = pathlib.Path("test-data/commentaries/jebb-ot")
URN_PREFIX = "urn:cts:greekLit:viaf2603144.viaf001.perseus-eng1"


def TEI(tag):
    return f"{{http://www.tei-c.org/ns/1.0}}{tag}"


def to_string(el):
    return re.sub(
        r"\s+", " ",
        etree.tostring(el, with_tail=True, encoding="utf-8", method="text").decode("utf-8")
    ).strip()


def get_glossae():
    tree = etree.parse(SRC_FILE)
    root = tree.getroot()

    commentary_div = root[1][0][0]
    assert commentary_div.tag == TEI("div")
    assert commentary_div.attrib["type"] == "commentary"
    # urn = commentary_div.attrib["n"]

    for child in commentary_div:
        assert child.tag == TEI("div")
        assert child.attrib["type"] == "textpart"
        assert child.attrib["subtype"] == "section"
        corresp = child.attrib["corresp"]

        for gchild in child:
            if gchild.tag == TEI("p"):
                yield (corresp, to_string(gchild))
            else:
                assert gchild.tag == TEI("div"), gchild.tag
                assert gchild.attrib["type"] == "textpart"
                assert gchild.attrib["subtype"] == "commline"
                if gchild.attrib.get("corresp"):
                    corresp2 = gchild.attrib["corresp"]
                else:
                    corresp2 = TEXT_URN + gchild.attrib["n"]
                yield (corresp2, to_string(gchild))

with open(DESTO_DIR / "glossae_001.jsonl", "w") as f:
    idx = 0
    for corresp, content in get_glossae():
        idx += 1
        entry = {
            "urn": f"{URN_PREFIX}:{idx}",
            "corresp": corresp,
            "content": content,
        }
        print(json.dumps(entry, ensure_ascii=False), file=f)

metadata = {
    "label": "Commentary on Sophocles: Oedipus Tyrannus by Sir Richard C. Jebb",
    "urn": URN_PREFIX,
    "kind": "Commentary",
    "entries": ["glossae_001.jsonl"],
}

with open(DESTO_DIR / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)
