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
        etree.tostring(el, with_tail=True, encoding="unicode", method="text")
    ).strip()

def to_xml(el):
    return re.sub(
        r"\s+", " ",
        etree.tostring(el, with_tail=True, encoding="unicode", method="xml")
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
                for ggchild in gchild:
                    assert ggchild.tag in [
                        TEI("foreign"),
                        TEI("emph"),
                        TEI("title"),
                        TEI("bibl"),
                    ], ggchild.tag
                yield (corresp, to_xml(gchild))
            else:
                assert gchild.tag == TEI("div"), gchild.tag
                assert gchild.attrib["type"] == "textpart"
                assert gchild.attrib["subtype"] == "commline"
                if gchild.attrib.get("corresp"):
                    corresp2 = gchild.attrib["corresp"]
                else:
                    corresp2 = TEXT_URN + gchild.attrib["n"]
                for ggchild in gchild:
                    assert ggchild.tag == TEI("p")
                    for gggchild in ggchild:
                        assert gggchild.tag in [
                            TEI("app"),
                            TEI("foreign"),
                            TEI("cit"),
                            TEI("emph"),
                            TEI("bibl"),
                            TEI("title"),
                        ], gggchild.tag
                yield (corresp2, to_xml(gchild))

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
