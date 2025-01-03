#!/usr/bin/env python

"""
Work-in-progress script to convert Middle Liddell to JSONL for Scaife ATLAS.

Note this treats each `div1` as a blob of plain text with no attempt (yet)
to retain formatting, extract senses or citations.
This will all come later (see LSJ).
"""

import json

from pathlib import Path
from lxml import etree

ML_REPO = Path("../../../MiddleLiddell")

URN_PREFIX = "urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:middle-liddell.perseus-eng2"

def to_string(el):
    return etree.tostring(el, with_tail=True, encoding="utf-8", method="text").decode("utf-8")

def get_entries(root):
    for entry in root.xpath("text//div1"):
        entry_orig_id = entry.attrib["orig_id"]
        entry_key = entry.attrib["key"]
        urn = f"{URN_PREFIX}-{entry_orig_id}"

        head = to_string(entry.xpath("head")[0]).split(",")[0].strip()
        contents = to_string(entry).strip()

        yield {
            "headword": head,
            "data": {
                "content": contents,
                "key": entry_key,
            },
            "urn": urn
        }


for filename in sorted(ML_REPO.glob("*.xml")):
    tree = etree.parse(filename)
    root = tree.getroot()

    num = filename.stem[-2:]

    with open(f"entries_{num:02}.jsonl", "w") as f:
        for entry in get_entries(root):
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")

