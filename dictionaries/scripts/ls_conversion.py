#!/usr/bin/env python

"""
Work-in-progress script to convert Lewis and Short to JSONL for Scaife ATLAS.

Note this treats the `entryFree` as a blob of plain text with no attempt (yet)
to retain formatting, extract senses or citations.
This will all come later (see LSJ).
"""

import json

from itertools import batched
from lxml import etree


FILENAME = "../../lexica/CTS_XML_TEI/perseus/pdllex/lat/ls/lat.ls.perseus-eng2.xml"

URN_PREFIX = "urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:lat.ls.perseus-eng2"


def to_string(el):
    return etree.tostring(el, with_tail=True, encoding="utf-8", method="text").decode("utf-8")

def get_entries(root):
    for entry in root.xpath("text/body/div0/entryFree"):
        entry_id = entry.attrib["id"]
        entry_type = entry.attrib["type"]
        entry_key = entry.attrib["key"]
        urn = f"{URN_PREFIX}-{entry_id}"

        orth = to_string(entry.xpath("orth")[0]).split(",")[0]
        contents = to_string(entry)

        yield {
            "headword": orth,
            "data": {
                "content": contents,
                "key": entry_key,
                "type": entry_type,
            },
            "urn": urn
        }

tree = etree.parse(FILENAME)

root = tree.getroot()

for batch_num, batch in enumerate(batched(get_entries(root), 10000), 1):
    with open(f"entries_{batch_num:03}.jsonl", "w") as f:
        for entry in batch:
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")

